# OpenSpec 操作手冊

> **適用版本**：v1.3.0
> **適用工具**：Claude Code（或其他 25+ 支援的 AI 工具）
> **更新日期**：2026-04-12

---

## 什麼是 OpenSpec

**Spec-Driven Development (SDD)** — 規格驅動開發框架。

核心理念：**先對齊規格，再開始實作**。在任何人 coding 之前，讓 Human 和 AI 先對「要做什麼」達成共識。

### 與傳統開發的差異

| 傳統方式 | OpenSpec 方式 |
|----------|---------------|
| 需求 → coding → 修改 → 再修改 | 需求 → **規格對齊** → Coding → 驗證 → 完成 |
| 規格漂移常見 | 規格是 source of truth |
| AI 容易誤解需求 | AI 參與規格制定，減少回頭重寫 |

---

## 快速開始

### 1. 初始化專案

```bash
cd your-project

# 初始化（選擇 AI 工具）
npx openspec init --tools claude
```

產生的結構：
```
專案/
├── openspec/
│   ├── specs/           # 主規格（source of truth）
│   │   └── archive/    # 已完成的規格歸檔
│   └── changes/       # 進行中的變更
│       └── archive/    # 已完成的變更歸檔
│
├── .claude/            # Claude Code 整合
│   ├── commands/       # 4 個指令
│   │   └── opsx       # /opsx:propose 等
│   └── skills/        # 4 個技能
│       ├── openspec-propose
│       ├── openspec-apply-change
│       ├── openspec-archive-change
│       └── openspec-explore
```

### 2. 重啟 Claude Code

初始化完成後，**重啟 Claude Code** 讓 slash commands 生效。

### 3. 啟動第一個 Change

在 Claude Code 中輸入：

```
/opsx:propose "你的想法"
```

---

## 工作流程

### 完整流程：4 個 Artifacts

```
┌─────────────┐
│  proposal   │  ← 需求提案（為什麼要做）
└──────┬──────┘
       ↓
┌──────┴──────┐
│   design    │  ← 技術設計（怎麼做）
└──────┬──────┘
       ↓
┌──────┴──────┐
│   specs     │  ← 詳細規格（做什麼）
└──────┬──────┘
       ↓
┌──────┴──────┐
│   tasks     │  ← 實作清單（具體步驟）
└─────────────┘
```

### Artifact 說明

| Artifact | 用途 | 回答問題 |
|----------|------|----------|
| **proposal.md** | 需求提案 | 為什麼要做？解決什麼問題？ |
| **design.md** | 技術設計 | 怎麼做？架構如何？風險？ |
| **specs/*.md** | 詳細規格 | 系統要做什麼？每個功能的需求？ |
| **tasks.md** | 實作清單 | 具體步驟是什麼？ |

---

## 常用指令

### 提出新變更

```
/opsx:propose "新功能名稱"
```

或使用 CLI：

```bash
npx openspec new change "feature-name"
```

### 實作任務

```
/opsx:apply feature-name
```

系統會逐一引導完成 tasks.md 中的任務。

### 查看狀態

```bash
npx openspec status --change "feature-name"
```

輸出範例：
```
Change: feature-name
Schema: spec-driven
Progress: 2/4 artifacts complete

[x] proposal
[x] design
[ ] specs
[-] tasks (blocked by: specs)
```

### 查看指令

```bash
npx openspec --help              # 總覽
npx openspec new --help          # new 子指令
npx openspec instructions --help  # 查看各 artifact 範本
```

---

## Change 命名規範

- **只能包含**：小寫字母、數字、連字符（`-`）
- **禁止**：空格、大寫字母、特殊符號

正確：`quarterly-margin-alert-system`
錯誤：`季度毛利率預警系統`、`QuarterlyMarginAlert`

---

## 規格檔案結構

### 預設結構（spec-driven schema）

```
openspec/changes/[change-name]/
├── .openspec.yaml      # Change 元資料
├── proposal.md         # 需求提案
├── design.md          # 技術設計
├── specs/             # 詳細規格
│   ├── capability-1/
│   │   └── spec.md
│   └── capability-2/
│       └── spec.md
└── tasks.md           # 實作清單
```

### specs/ 命名

- 來自 proposal.md 的 Capabilities 區段
- 使用 **kebab-case**（小寫、連字符）
- 每個 capability 一個資料夾 + spec.md

---

## 實作迴圈

### 標準流程

```
1. /opsx:propose "新功能"
   → 建立 proposal.md

2. 撰寫 proposal.md
   → 回答：為什麼要做？改變什麼？

3. /opsx:continue
   → 解除 design 封鎖

4. 撰寫 design.md
   → 回答：怎麼做？架構？風險？

5. /opsx:continue
   → 解除 specs 封鎖

6. 撰寫 specs/*.md
   → 回答：每個功能要做什麼？場景？

7. /opsx:continue
   → 解除 tasks 封鎖

8. 撰寫 tasks.md
   → 回答：具體步驟？

9. /opsx:apply
   → 開始實作
```

### 被打斷怎麼辦

```
# 查看目前狀態
/opsx:status

# 繼續當前任務
/opsx:continue

# 查看待完成項目
openspec status --change "feature-name"
```

---

## 與 Claude Code 協作

### Slash Commands

| 指令 | 功能 |
|------|------|
| `/opsx:propose [name]` | 提議新變更 |
| `/opsx:apply [name]` | 實作任務 |
| `/opsx:archive [name]` | 歸檔完成 |
| `/opsx:continue` | 繼續當前任務 |
| `/opsx:status` | 查看狀態 |
| `/opsx:explore` | 探索現有結構 |

### CLAUDE.md 整合

OpenSpec 會在 `.claude/` 建立技能檔案。Claude Code 啟動時自動讀取。

---

## 最佳實踐

### 1. Proposal 要簡潔

- 專注「為什麼」，不是「怎麼做」
- 1-2 頁即可
- 具體說明改變什麼、新增什麼

### 2. Specs 要可測試

- 每個需求要有場景（Scenario）
- 場景用 `WHEN` / `THEN` 格式
- 好的 spec 可以直接轉換為測試案例

### 3. Tasks 要小到可完成

- 每個任務 15-30 分鐘內可完成
- 有明確的完成標準
- 按依賴順序排列

### 4. 不要追求完美

- OpenSpec 是**fluid** 的
- 可以隨時回頭修改 artifact
- 迭代比完美重要

---

## 疑難排解

### Q: `--tools` 選項不存在？

```bash
# 正確方式
npx openspec init --tools claude

# 錯誤（舊版本語法）
npx openspec init --tool claude  # ❌
```

### Q: Change 命名失敗？

```
Error: Change name can only contain lowercase letters, numbers, and hyphens
```

**解決**：使用 kebab-case（全小寫、連字符）

```bash
# 錯誤
npx openspec new change "季度毛利率預警"

# 正確
npx openspec new change "quarterly-margin-alert"
```

### Q: 忘記目前狀態？

```bash
npx openspec list
```

### Q: 想放棄目前的 Change？

```bash
# 查看所有 changes
npx openspec list

# 刪除（手動）
rm -rf openspec/changes/[change-name]
```

### Q: Specs 被打斷？

```
[tasks] blocked by: design, specs
```

**原因**：tasks 依賴 design 和 specs 完成。

**解決**：完成被打斷的 artifact，然後 `openspec status --change "name"` 更新進度。

---

## 與現有專案整合

### 建議採用策略

**Phase 1（1-2 週）：單一專案試點**
- 選擇一個中等規模的功能開始
- 只對「新增功能」使用 OpenSpec
- 簡單修改維持直接 coding

**Phase 2（持續）：逐步擴展**
- 複雜功能優先用 OpenSpec
- 建立團隊共識

**Phase 3（可選）：團隊標準化**
- 制定團隊 `specs/` 結構規範
- 與 Git workflow 整合

---

## 相關資源

- **官方文件**：https://github.com/Fission-AI/OpenSpec
- **支援的工具**：25+ AI assistants（Claude, Cursor, GitHub Copilot, Gemini, Windsurf 等）
- **本專案落地**：已在「新增資料夾」初始化

---

## 更新紀錄

| 日期 | 版本 | 內容 |
|------|------|------|
| 2026-04-12 | v1.0 | 初始版本 |

---

*本手冊基於 OpenSpec v1.3.0 編寫*
