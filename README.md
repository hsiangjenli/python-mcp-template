# python-mcp-template

## 需求與待辦事項

### 開發環境
- [x] 建立 Dockerfile，方便部署與環境一致性
- [x] 使用 uv 管理 Python 版本與依賴
- [ ] 整合 CI/CD（如 GitHub Actions）自動化流程
   - [ ] Trigger: Tag push
   - [ ] 在 GitHub 上建立 Docker image 並推送到 Docker Hub
   - [ ] 在 GitHub 上建立 Release
   - [ ] Auto Changelog
   - [ ] 自動建立 GitHub Pages 網站
- [x] 改用 rye 來 format python 程式

### 程式碼品質
- [x] API schema 驗證（pydantic）
- [ ] 程式碼安全檢查（如 bandit）

### 測試與文件
- [x] 建立 Restful API，符合 MCP 標準
- [ ] 快速建立自動化文件（Documentation），如使用 Sphinx 或 MkDocs (Need to fix, due to `mcp_tools` not being a package, and schemas not being imported correctly)
- [ ] 快速建立單元測試（Unit Test），建議使用 pytest
- [ ] 程式碼覆蓋率報告（如 coverage.py）

### Improvements
- [ ] 在 MCP Server 中使用 `docker run` 來啟動容器，免去手動啟動的麻煩

## MCP Server 

### Local Development

- https://gofastmcp.com/patterns/cli

```bash
uv run --with fastmcp fastmcp run mcp_tools/main.py
```

### Docker

```shell
"mymcp": {
    "type": "stdio",
    "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "python-mcp-template:fastmcp-latest",
        ],
    }
```

## Documentation

```bash
scripts/build_docs.sh
mkdocs serve
```

![20250711222517](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250711222517.png)