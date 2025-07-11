# python-mcp-template

## 需求與待辦事項

### 開發環境
- [ ] 建立 Dockerfile，方便部署與環境一致性
- [x] 使用 uv 管理 Python 版本與依賴
- [ ] 整合 CI/CD（如 GitHub Actions）自動化流程
- [x] 改用 rye 來 format python 程式

### 程式碼品質
- [x] API schema 驗證（pydantic）
- [ ] 程式碼安全檢查（如 bandit）

### 測試與文件
- [x] 建立 Restful API，符合 MCP 標準
- [x] 快速建立自動化文件（Documentation），如使用 Sphinx 或 MkDocs
- [ ] 快速建立單元測試（Unit Test），建議使用 pytest
- [ ] 程式碼覆蓋率報告（如 coverage.py）

## RUN

```bash
uvicorn mcp_tools.main:app --reload
```

## Documentation

```bash
scripts/build_docs.sh
mkdocs serve
```

![20250711222517](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250711222517.png)