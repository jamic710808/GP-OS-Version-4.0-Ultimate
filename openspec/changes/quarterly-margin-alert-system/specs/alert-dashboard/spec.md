# Alert Dashboard Specification

## ADDED Requirements

### Requirement: Alert Dashboard Page
系統 SHALL 提供「預警中心」頁面作為第 15 個 Tab，包含以下區塊：
- 預警摘要卡片（總數、待處理、已處理）
- 異常清單（可依維度篩選）
- 預警規則設定面板

### Requirement: Alert Summary Cards
預警摘要 SHALL 顯示以下資訊：
- **總預警數**: 所有狀態的預警數量
- **待處理**: 狀態為 'triggered' 的數量
- **已處理**: 狀態為 'acknowledged' 或 'resolved' 的數量

### Requirement: Alert List Display
異常清單 SHALL 以表格形式顯示，欄位包含：
- 維度圖標（產品/客戶/地區/渠道）
- 目標名稱
- 預警原因（低於下限/高於上限）
- 發生時間
- 狀態標籤
- 操作按鈕（確認/解決）

### Requirement: Filter by Dimension
使用者 SHALL 能夠依維度篩選預警清單（MUST support 'all' | 'product' | 'customer' | 'region' | 'channel'）。

#### Scenario: Filter by product dimension
- **WHEN** 使用者選擇「產品」維度篩選
- **THEN** 清單 SHALL 僅顯示產品維度的預警

### Requirement: Alert Rule Configuration Panel
預警規則設定面板 SHALL 支援：
- 新增規則（選擇維度、目標、輸入閾值）
- 編輯現有規則
- 刪除規則
- 啟用/停用規則

### Requirement: Visual Highlight
當前頁面存在異常資料時，系統 SHALL 在對應的 Tab 標題顯示紅點提示。

#### Scenario: Tab shows alert indicator
- **WHEN** 任意產品毛利率異常
- **THEN** 「毛利瀑布分解」Tab SHALL 顯示紅點
- **AND** 使用者點擊可快速跳轉至預警中心

### Requirement: Empty State
當無任何預警時，清單 SHALL 顯示「目前無異常」訊息。
