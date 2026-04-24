## Why

目前毛利分析 V3.0 缺乏主動預警機制，管理層只能在事後查看報告，無法在毛利異常發生時即時察覺。新增季度毛利率預警系統可在毛利率偏離目標時自動提醒相關人員，將被動分析轉化為主動監控。

## What Changes

- 新增「預警中心」頁面，顯示所有異常狀態
- 設定毛利率閾值（上下限），超限時高亮顯示
- 支援 Email/Webhook 通知（可設定通知對象）
- 預警記錄歷史追蹤
- 支援多維度預警：產品、客戶、地區、渠道

## Capabilities

### New Capabilities
- `margin-alert`: 毛利率預警核心邏輯，包含閾值設定、異常判定、通知觸發
- `alert-dashboard`: 預警中心儀表板，即時顯示所有異常狀態
- `alert-history`: 預警記錄查詢，支援歷史趨勢分析

### Modified Capabilities
- 無（目前無預警相關功能）

## Impact

- 新增頁面：預警中心
- 影響現有 Tab 結構（需在 Tab 列表新增「預警中心」）
- 新增通知模組相依性（Email/Webhook）
- 資料結構擴展：AlertRecord 類型
