# Alert History Specification

## ADDED Requirements

### Requirement: History Storage
系統 SHALL 使用 localStorage 儲存預警記錄，Key 為 `marginAlertHistory`，Value 為 JSON 陣列。

### Requirement: History Limit
localStorage 儲存的 AlertRecord 數量 SHALL 限制為 1000 筆，當超過時 SHALL 自動刪除最舊的記錄。

### Requirement: History Query
系統 SHALL 支援查詢歷史預警記錄，可依以下條件篩選：
- 時間範圍（起訖日期）
- 維度類型
- 預警狀態
- 目標 ID

### Requirement: History Export
使用者 SHALL 能夠匯出預警記錄為 CSV 格式。

#### Scenario: Export history to CSV
- **WHEN** 使用者點擊「匯出」按鈕
- **THEN** 系統 SHALL 下載包含所有符合條件記錄的 CSV 檔案
- **AND** CSV SHALL 包含欄位：時間、維度、目標名稱、預警原因、當時毛利率、狀態

### Requirement: History Trend Chart
預警中心 SHALL 顯示預警趨勢圖（過去 12 期的預警數量折線圖）。

#### Scenario: Display trend chart
- **WHEN** 使用者開啟預警中心
- **THEN** 系統 SHALL 顯示折線圖，X 軸為月份，Y 軸為預警數量

### Requirement: Alert Status Update
使用者 SHALL 能夠更新預警狀態：
- **triggered** → **acknowledged**（已讀取）
- **acknowledged** → **resolved**（已處理）

#### Scenario: Acknowledge alert
- **WHEN** 使用者點擊「確認」按鈕
- **THEN** 該 AlertRecord 的狀態 SHALL 更新為 'acknowledged'
- **AND** localStorage SHALL 同步更新

### Requirement: Bulk Operations
使用者 SHALL 能夠一次確認或解決多筆預警。

#### Scenario: Bulk acknowledge
- **WHEN** 使用者勾選多筆預警並點擊「批量確認」
- **THEN** 所有勾選記錄的狀態 SHALL 同時更新為 'acknowledged'
