# AGENT 指南（Python MCP Template）

本文件提供給 AI 代理與人類開發者，用於快速理解、啟動與擴充此專案的 MCP 伺服器。專案以 FastAPI + fastmcp 為核心，將既有的 OpenAPI 規格映射成 MCP 工具，並以 MkDocs 產生文件。

## 專案概覽
- 核心目標：以最小樣板快速建立符合 Model Context Protocol（MCP）的伺服器。
- 主要技術：`FastAPI`、`fastmcp`、`Pydantic`、`MkDocs`、`uv`（套件與環境管理）。
- 入口與關鍵檔案：
  - 伺服器入口：`mcp_tools/main.py`
  - 資料模型：`mcp_tools/schemas.py`
  - 文件腳本：`scripts/export_openapi.py`、`scripts/openapi_to_markdown.py`
  - 文件來源：`docs/`（`openapi.json`、`reference/` 等）
  - 發佈與自動化：`.github/workflows/docker_image.yaml`、`.github/workflows/github_pages.yaml`
  - 容器化：`Dockerfile`

## 如何執行（本地 / Docker / MCP 客戶端）
- 本地（建議使用 uv）
  1) 安裝相依：`uv sync`
  2) 啟動 MCP 伺服器：`uv run --with fastmcp fastmcp run mcp_tools/main.py`
- Docker
 - 建置：`docker build -t python-mcp-template:latest .`
  - 執行：`docker run -i --rm -p 8000:8000 python-mcp-template:latest`
    - 備註：預設使用 MCP `stdio` 傳輸，不需對外開放 8000；若改以 `uvicorn mcp_tools.main:app` 提供 HTTP，再使用 `-p 8000:8000`。
- Claude Desktop（MCP 設定片段）
  ```json
  {
    "mcpServers": {
      "python-mcp-template": {
        "command": "docker",
        "args": [
          "run", "--rm", "-i", "-p", "8000:8000", "python-mcp-template:latest"
        ]
      }
    }
  }
  ```

說明：此專案使用 `fastmcp run` 將 FastAPI 應用包裝成 MCP 伺服器。若需 HTTP 形式的 FastAPI 服務，請以 `uvicorn mcp_tools.main:app` 自行啟動（本樣板預設專注於 MCP）。

## 已提供的 MCP 工具 / API 端點
- `new_endpoint`（POST `/new/endpoint/`，`operation_id="new_endpoint"`）
  - 請求模型：`NewEndpointRequest`（欄位：`name: str`）
  - 回應模型：`NewEndpointResponse`（欄位：`message: str`）
  - 範例請求：
    ```json
    { "name": "developer" }
    ```
  - 範例回應：
    ```json
    { "message": "Hello, developer!" }
    ```
  - 原始碼位置：`mcp_tools/main.py`、`mcp_tools/schemas.py`

更完整的端點與模型說明可參考：
- 文件首頁：`docs/index.md`
- 端點文件：`docs/reference/endpoints.md`
- 模型文件：`docs/reference/models.md`

## 擴充指南（新增一個端點）
1) 在 `mcp_tools/schemas.py` 定義請求與回應的 Pydantic 模型，補上 `description`、`example` 以利產生文件。
2) 在 `mcp_tools/main.py` 新增對應的 FastAPI 路由：
   - 指定 `operation_id`（作為 MCP 工具名稱，請保持穩定命名）。
   - 指定 `response_model` 以輸出正確的 schema。
3) 產生/更新文件（OpenAPI → Markdown）：
   - `chmod +x scripts/build_docs.sh`
   - `scripts/build_docs.sh`
   - 輸出包括：`docs/openapi.json`、`docs/reference/endpoints.md`、`docs/reference/models.md`
4) 驗證與測試：
   - 本專案已採用 `pytest`。新增或變更端點時，請在 `tests/` 補上對應測試（成功與錯誤路徑），可參考 `tests/test_api.py`。

實作小抄：
- 命名：`operation_id` 使用簡短、具語意的 snake_case，如 `create_user`。
- 模型：以必填與型別精準度為優先，附上 `description` 與 `example` 提升可讀性。
- 文件：變更端點後務必重跑文件腳本，保持 `docs/` 與程式碼同步。

## 文件與發佈自動化
- MkDocs 設定：`mkdocs.yml`
  - 導航包含：首頁、端點與資料模型頁面，並使用 `neoteroi.mkdocsoad` 顯示 OpenAPI 內容。
- CI/CD
  - Docker 映像：`.github/workflows/docker_image.yaml`（push 到 `main` 觸發，推送到 Docker Hub）。
  - GitHub Pages：`.github/workflows/github_pages.yaml`（推 `v*` tag 觸發，建置並發佈文件到 Pages）。
- 釋出流程（範例）：
  - 合併到 `main` → 自動建置與推送 Docker 映像。
  - 建立 tag（例如 `v0.2.0`）→ 自動產生並部署文件站台。

## 開發約定
- Python 版本：`3.12`（見 `pyproject.toml`）。
- 依賴管理：`uv`；請優先使用 `uv add`、`uv sync`、`uv run`。
- 程式風格：維持與現有程式碼一致；提供型別標註與適當的 docstring。
- 程式碼格式：開發完成後請執行 `rye format <path>`（例如：`rye format mcp_tools/main.py`、`rye format tests/test_api.py`），再進行提交。
- 安全掃描：開發完成後請以 `bandit` 進行靜態掃描，避免明顯安全問題，並根據掃描結果進行修復。
  - 安裝（一次性）：`uv add --dev bandit`
  - 掃描範圍（範例）：`uv run bandit -r mcp_tools scripts tests`（或 `uv run bandit -r .`）
  - 本地執行腳本（同 CI）：`uv run bash scripts/security_scan_bandit.sh` 之後檢視 `bandit-report.txt` 並修復。
- 變更範圍：聚焦與需求相關；避免不必要的重構或重新命名公共 API。
- 文件同步：每次調整端點/模型後，務必重新輸出 `openapi.json` 並更新 MkDocs。

## 單元測試規範
- 標準測試框架：採用 `pytest` 作為執行器與風格（例見 `tests/test_api.py`）。
- 強制規範：每開發一個新的 API 都要寫對應的單元測試（成功路徑與錯誤路徑皆需覆蓋）。
- 測試位置：`tests/` 目錄下，檔名建議 `test_<feature>.py`；使用 `fastapi.testclient.TestClient`。
- 本地執行：
  - 新增測試相依（一次性）：`uv add --dev pytest coverage`
  - 只跑測試：`uv run -m pytest -q`
  - 帶覆蓋率：
    - `uv run coverage run -m pytest -q`
    - `uv run coverage report -m --fail-under=80`
    - `uv run coverage html`（輸出 `htmlcov/` 可在本地開啟 `htmlcov/index.html`）
- API 測試要點：
  - 斷言狀態碼與回傳 JSON 結構；對 4xx/5xx 的錯誤訊息也要覆蓋。
  - 邊界條件（空字串、超長、特殊字元）與驗證錯誤（422）。
  - 若呼叫外部服務，請使用 `unittest.mock` 或 `pytest` fixture 進行 mock，保持測試可重現與離線。
  - 測試命名採 Arrange-Act-Assert 思維，保持獨立、可讀。

標準化說明：本專案以 pytest 作為測試執行器（runner）。即便 `unittest` 風格的測試也能被 pytest 收斂，但建議以 pytest 風格撰寫以保持一致性（範例見 `tests/test_api.py`）。

## CI/CD 測試（含覆蓋率）
- 工作流程檔：`.github/workflows/unitest.yaml`
  - 觸發條件：push 與 pull_request 至 `main`。
  - 測試執行：以 `pytest` 執行，並用 `coverage` 產生覆蓋率報告。
  - 覆蓋率門檻：透過環境變數 `COVERAGE_FAIL_UNDER` 控制（預設 80）。
  - 產出物：`coverage.xml`、`htmlcov/`、`pytest-report.xml` 會以 Artifacts 上傳，於 GitHub Actions 工作流程頁面查看。
- 本地對應指令（與 CI 一致）：見上節「單元測試規範 > 本地執行」。

安全掃描（Bandit）在 CI 中
- 工作流程會呼叫 `scripts/security_scan_bandit.sh` 產生 `bandit-report.txt` 並將摘要寫入 GitHub Step Summary。
- 隨後呼叫 `scripts/security_fail_if_issues.sh`；若 Bandit 找到問題，工作流程會標記失敗。

略過（Suppress）規則與設定方式
- 單行忽略：在該行尾加上 `# nosec`，並附理由供 Code Review（例如：`# nosec - false positive, input validated above`）。
- 跳過特定規則：使用 `-s` 參數，例如 `bandit -s B101,B603 -r .`。
- 排除路徑：使用 `-x` 參數，例如 `bandit -x tests,examples -r .`。
- 設定檔：建立 `bandit.yaml` 並以 `-c bandit.yaml` 指定，集中管理規則與排除。
  - 範例（`bandit.yaml`）
    ```yaml
    skips: ["B101", "B603"]
    exclude_dirs: ["tests", "examples"]
    severity: "LOW"       # or MEDIUM/HIGH（最低嚴重度門檻）
    confidence: "LOW"     # or MEDIUM/HIGH（最低信心門檻）
    ```
  - 專案層級使用方式：`uv run bandit -c bandit.yaml -r .`

## 開發相依（dev dependencies）
- 使用 `uv add --dev` 同步開發相依，範例：
  - `uv add --dev pytest coverage bandit`
- 建議在本地開發流程中：
  - 格式檢查：`rye format <path>`
  - 安全掃描：`uv run bandit -r mcp_tools scripts tests`
 - 專案已在 `pyproject.toml` 的 `[tool.uv]` 設定 `dev-dependencies`（pytest、coverage、bandit）。
   - 本地同步所有相依：`uv sync`
   - 僅同步非開發相依：`uv sync --no-dev`

CI 安裝說明（pytest 要安裝對）
- 在 `.github/workflows/unitest.yaml` 內以 `pip install . pytest coverage bandit` 安裝測試與安全掃描所需套件，確保 CI 能正確執行 pytest、coverage 與 bandit。

### 套件安裝指引（使用 uv add）
- 新增一般依賴：
  - `uv add fastapi`（會更新 `pyproject.toml` 與 `uv.lock`，並安裝到 `.venv`）
- 新增開發依賴：
  - `uv add --dev pytest`、`uv add --dev ruff`、`uv add --dev bandit`
- 安裝既有相依（鎖檔）：
  - `uv sync`（遵循 `uv.lock`）
- 執行指令：
  - `uv run <command>`（例如：`uv run --with fastmcp fastmcp run mcp_tools/main.py`）

## 常見工作流程範例
- 新增端點：
  1) 新增/更新 Pydantic 模型（`mcp_tools/schemas.py`）
  2) 新增 FastAPI 路由（`mcp_tools/main.py`，設定 `operation_id`/`response_model`）
  3) 產生文件（`scripts/build_docs.sh`）並檢查 `docs/reference/*.md`
  4) 驗證在 MCP 客戶端中可使用（例如 Claude Desktop）

## 參考連結（檔案）
- 入口：`mcp_tools/main.py`
- 模型：`mcp_tools/schemas.py`
- 文件腳本：`scripts/export_openapi.py`、`scripts/openapi_to_markdown.py`
- MkDocs 設定：`mkdocs.yml`
- README：`README.md`
- Dockerfile：`Dockerfile`
- GitHub Actions：`.github/workflows/docker_image.yaml`、`.github/workflows/github_pages.yaml`

---
若需要我幫你新增端點、調整文件或設定 CI/CD，請告訴我具體需求與預期輸入/輸出，我會直接幫你改好並同步更新文件。
