# Margin Alert Specification

## ADDED Requirements

### Requirement: Alert Rule Structure
系統 SHALL 支援毛利率預警規則，規則包含以下屬性：
- `id`: 唯一識別碼
- `dimension`: 維度類型（MUST be 'product' | 'customer' | 'region' | 'channel'）
- `targetId`: 目標 ID（對應維度的特定項目）
- `minMargin`: 毛利率下限（NULL 表示不限制）
- `maxMargin`: 毛利率上限（NULL 表示不限制）
- `enabled`: 是否啟用

### Requirement: Alert Triggering
當系統載入資料或使用者變更篩選條件時，系統 SHALL 對每個已啟用的規則執行以下檢查：
- 若 `actualMargin < minMargin`，則觸發「低於下限」預警
- 若 `actualMargin > maxMargin`，則觸發「高於上限」預警

### Requirement: Alert Record Creation
當預警觸發時，系統 SHALL 建立 AlertRecord 並儲存至 localStorage，Record 包含：
- `id`: 唯一識別碼
- `ruleId`: 關聯的規則 ID
- `timestamp`: 觸發時間
- `actualMargin`: 當時毛利率
- `status`: 預警狀態（MUST be 'triggered' | 'acknowledged' | 'resolved'）

### Requirement: Alert Notification
當預警觸發且通知功能已啟用時，系統 SHALL 嘗試傳送 Email 通知至設定的收件人。

#### Scenario: Low margin alert triggered
- **WHEN** 某產品的毛利率為 18%，而設定的下限為 20%
- **THEN** 系統 SHALL 觸發預警並建立 AlertRecord
- **AND** 系統 SHALL 嘗試傳送 Email 通知（若已啟用）

#### Scenario: High margin alert triggered
- **WHEN** 某客戶的毛利率為 35%，而設定的上限為 30%
- **THEN** 系統 SHALL 觸發預警並建立 AlertRecord
- **AND** 系統 SHALL 嘗試傳送 Email 通知（若已啟用）

#### Scenario: Margin within threshold
- **WHEN** 某產品的毛利率為 22%，設定範圍為 20%~25%
- **THEN** 系統 SHALL NOT 觸發任何預警

### Requirement: Multiple Threshold Support
單一維度目標 SHALL 支援多個預警規則（同時檢查多個條件）。

#### Scenario: Same product multiple rules
- **WHEN** 產品 A 同時有規則：下限 15% 和下限 20%
- **AND** 實際毛利率為 18%
- **THEN** 系統 SHALL 觸發「低於 20%」預警
- **AND** 系統 SHALL NOT 觸發「低於 15%」預警
