# FINRA Query API Inventory

Generated from the official FINRA Developer Center documentation and public metadata endpoints.

Sources:
- https://developer.finra.org/products/query-api
- https://developer.finra.org/docs
- https://developer.finra.org/catalog
- https://api.finra.org/datasets
- https://api.finra.org/metadata/group/{group}/name/{dataset}

Scope: FINRA Query API read-only datasets only. Submission API, Notification API, fileX, and write operations are excluded.

Endpoint patterns:
- Dataset search: `/datasets`
- Query data: `/data/group/{group}/name/{dataset}`
- Single record: `/data/group/{group}/name/{dataset}/id/{id}`
- Metadata: `/metadata/group/{group}/name/{dataset}`
- Async status: `/async-requests/{requestId}`
- Async result: `/async-requests/{requestId}/result`

Discovered logical dataset sections: 41
Discovered dataset names including mock/historic variants: 80

## Equity (`otcMarket`)

### Blocks Summary (`blocksSummary`)

- Dataset group: `otcMarket`
- Description: Aggregated ATS trade data in NMS stocks that meets certain share based and dollar based thresholds.
- Documentation: https://developer.finra.org/docs#query_api-equity-blocks_summary
- Endpoint pattern: `/data/group/otcMarket/name/{dataset}`
- Metadata endpoint: `/metadata/group/otcMarket/name/{dataset}`
- Partition fields: `monthStartDate`
- Dataset names:
  - `blocksSummary` (production): data `/data/group/otcMarket/name/blocksSummary`, metadata `/metadata/group/otcMarket/name/blocksSummary`
    - Available fields: `MPID`, `marketParticipantName`, `summaryStartDate`, `totalTradeCount`, `totalShareQuantity`, `averageTradeSize`, `averageTradeSizeRank`, `ATSTradeRank`, `ATSShareRank`, `ATSTradePercent`, `ATSSharePercent`, `ATSBlockCount`, `ATSBlockQuantity`, `averageBlockSize`, `averageBlockSizeRank`, `ATSBlockTradeRank`, `ATSBlockShareRank`, `ATSBlockTradePercent`, `ATSBlockSharePercent`, `ATSBlockBusinessTradePercent`, `ATSBlockBusinessSharePercent`, `ATSBlockBusinessTradeRank`, `ATSBlockBusinessShareRank`, `summaryTypeCode`, `summaryTypeDescription` (+5 more)
  - `blocksSummaryMock` (mock): data `/data/group/otcMarket/name/blocksSummaryMock`, metadata `/metadata/group/otcMarket/name/blocksSummaryMock`
    - Available fields: `MPID`, `marketParticipantName`, `summaryStartDate`, `totalTradeCount`, `totalShareQuantity`, `averageTradeSize`, `averageTradeSizeRank`, `ATSTradeRank`, `ATSShareRank`, `ATSTradePercent`, `ATSSharePercent`, `ATSBlockCount`, `ATSBlockQuantity`, `averageBlockSize`, `averageBlockSizeRank`, `ATSBlockTradeRank`, `ATSBlockShareRank`, `ATSBlockTradePercent`, `ATSBlockSharePercent`, `ATSBlockBusinessTradePercent`, `ATSBlockBusinessSharePercent`, `ATSBlockBusinessTradeRank`, `ATSBlockBusinessShareRank`, `summaryTypeCode`, `summaryTypeDescription` (+5 more)

### Consolidated Short Interest (`consolidatedShortInterest`)

- Dataset group: `otcMarket`
- Description: The Consolidated Short Interest data provides a single view of OTC short interest positions submissions across all exchanges.
- Documentation: https://developer.finra.org/docs#query_api-equity-consolidated_short_interest
- Endpoint pattern: `/data/group/otcMarket/name/{dataset}`
- Metadata endpoint: `/metadata/group/otcMarket/name/{dataset}`
- Partition fields: `settlementDate`
- Dataset names:
  - `consolidatedShortInterest` (production): data `/data/group/otcMarket/name/consolidatedShortInterest`, metadata `/metadata/group/otcMarket/name/consolidatedShortInterest`
    - Available fields: `accountingYearMonthNumber`, `symbolCode`, `issueName`, `issuerServicesGroupExchangeCode`, `marketClassCode`, `currentShortPositionQuantity`, `previousShortPositionQuantity`, `stockSplitFlag`, `averageDailyVolumeQuantity`, `daysToCoverQuantity`, `revisionFlag`, `changePercent`, `changePreviousNumber`, `settlementDate`
  - `consolidatedShortInterestMock` (mock): data `/data/group/otcMarket/name/consolidatedShortInterestMock`, metadata `/metadata/group/otcMarket/name/consolidatedShortInterestMock`
    - Available fields: `accountingYearMonthNumber`, `symbolCode`, `issueName`, `issuerServicesGroupExchangeCode`, `marketClassCode`, `currentShortPositionQuantity`, `previousShortPositionQuantity`, `stockSplitFlag`, `averageDailyVolumeQuantity`, `daysToCoverQuantity`, `revisionFlag`, `changePercent`, `changePreviousNumber`, `settlementDate`

### Monthly Summary (`monthlySummary`)

- Dataset group: `otcMarket`
- Description: Monthly aggregate trade data for OTC (non-ATS) trading data for each firm with trade reporting obligations under FINRA rules.
- Documentation: https://developer.finra.org/docs#query_api-equity-monthly_summary
- Endpoint pattern: `/data/group/otcMarket/name/{dataset}`
- Metadata endpoint: `/metadata/group/otcMarket/name/{dataset}`
- Partition fields: `monthStartDate`, `tierIdentifier`
- Dataset names:
  - `monthlySummary` (production): data `/data/group/otcMarket/name/monthlySummary`, metadata `/metadata/group/otcMarket/name/monthlySummary`
    - Available fields: `issueSymbolIdentifier`, `issueName`, `firmCRDNumber`, `marketParticipantName`, `tierIdentifier`, `summaryStartDate`, `totalMonthlyTradeCount`, `totalMonthlyShareQuantity`, `productTypeCode`, `summaryTypeCode`, `monthStartDate`, `lastUpdateDate`, `initialPublishedDate`, `lastReportedDate`, `totalNotionalSum`
  - `monthlySummaryMock` (mock): data `/data/group/otcMarket/name/monthlySummaryMock`, metadata `/metadata/group/otcMarket/name/monthlySummaryMock`
    - Available fields: `issueSymbolIdentifier`, `issueName`, `firmCRDNumber`, `marketParticipantName`, `tierIdentifier`, `summaryStartDate`, `totalMonthlyTradeCount`, `totalMonthlyShareQuantity`, `productTypeCode`, `summaryTypeCode`, `monthStartDate`, `lastUpdateDate`, `initialPublishedDate`, `lastReportedDate`

### OTC Block Summary (`otcBlocksSummary`)

- Dataset group: `otcMarket`
- Description: Aggregated OTC (Non-ATS) trade data in NMS stocks that meets certain share based and dollar based thresholds.
- Documentation: https://developer.finra.org/docs#query_api-equity-otc_block_summary
- Endpoint pattern: `/data/group/otcMarket/name/{dataset}`
- Metadata endpoint: `/metadata/group/otcMarket/name/{dataset}`
- Partition fields: `monthStartDate`
- Dataset names:
  - `otcBlocksSummary` (production): data `/data/group/otcMarket/name/otcBlocksSummary`, metadata `/metadata/group/otcMarket/name/otcBlocksSummary`
    - Available fields: `crdFirmName`, `summaryStartDate`, `totalTradeCount`, `totalShareQuantity`, `averageTradeSize`, `averageTradeSizeRank`, `OTCTradeRank`, `OTCShareRank`, `OTCTradePercent`, `OTCSharePercent`, `OTCBlockCount`, `OTCBlockQuantity`, `averageBlockSize`, `averageBlockSizeRank`, `OTCBlockTradeRank`, `OTCBlockShareRank`, `OTCBlockTradePercent`, `OTCBlockSharePercent`, `OTCBlockBusinessTradePercent`, `OTCBlockBusinessSharePercent`, `OTCBlockBusinessTradeRank`, `OTCBlockBusinessShareRank`, `summaryTypeCode`, `summaryTypeDescription`, `monthStartDate` (+4 more)
  - `otcBlocksSummaryMock` (mock): data `/data/group/otcMarket/name/otcBlocksSummaryMock`, metadata `/metadata/group/otcMarket/name/otcBlocksSummaryMock`
    - Available fields: `crdFirmName`, `summaryStartDate`, `totalTradeCount`, `totalShareQuantity`, `averageTradeSize`, `averageTradeSizeRank`, `OTCTradeRank`, `OTCShareRank`, `OTCTradePercent`, `OTCSharePercent`, `OTCBlockCount`, `OTCBlockQuantity`, `averageBlockSize`, `averageBlockSizeRank`, `OTCBlockTradeRank`, `OTCBlockShareRank`, `OTCBlockTradePercent`, `OTCBlockSharePercent`, `OTCBlockBusinessTradePercent`, `OTCBlockBusinessSharePercent`, `OTCBlockBusinessTradeRank`, `OTCBlockBusinessShareRank`, `summaryTypeCode`, `summaryTypeDescription`, `monthStartDate` (+4 more)

### OTC Daily List (`otcDailyList`)

- Dataset group: `otcMarket`
- Description: OTC Daily List
- Documentation: https://developer.finra.org/docs#query_api-equity-otc_daily_list
- Endpoint pattern: `/data/group/otcMarket/name/{dataset}`
- Metadata endpoint: `/metadata/group/otcMarket/name/{dataset}`
- Partition fields: `calendarDay`
- Dataset names:
  - `otcDailyList` (production): data `/data/group/otcMarket/name/otcDailyList`, metadata `/metadata/group/otcMarket/name/otcDailyList`
    - Available fields: `oldOATSReportableFlag`, `newSymbolCode`, `ADRWitholdingTaxPercentage`, `oldADROrdinaryShareRate`, `newSecurityDescription`, `subjectCorporateActionCode`, `oldRegFeeFlag`, `dailyListReasonDescription`, `changeRoundLotQuantityFlag`, `bankruptcyFlag`, `changeSecurityDescriptionFlag`, `changeOATSReportableFlag`, `stockPercentage`, `newOATSReportableFlag`, `newFinancialStatusCode`, `qualifiedDividendDescription`, `newClassText`, `oldSecurityDescription`, `offeringTypeDescription`, `oldClassText`, `dividendTypeDescription`, `ADRNetRate`, `newRegFeeFlag`, `dailyListEventCode`, `ADRFeeAmount` (+35 more)
  - `otcDailyListMock` (mock): data `/data/group/otcMarket/name/otcDailyListMock`, metadata `/metadata/group/otcMarket/name/otcDailyListMock`; notes: HTTP 404
    - Available fields: not discoverable in the unauthenticated generation run; call metadata with authorized credentials.

### Reg SHO Daily Short Sale Volume (`regShoDaily`)

- Dataset group: `otcMarket`
- Description: Daily short sale aggregated volume by security for all short sale trades executed and reported to a FINRA trade reporting facility. API Explorer (Playground) TEST IT OUT
- Documentation: https://developer.finra.org/docs#query_api-equity-reg_sho_daily_short_sale_volume
- Endpoint pattern: `/data/group/otcMarket/name/{dataset}`
- Metadata endpoint: `/metadata/group/otcMarket/name/{dataset}`
- Partition fields: `tradeReportDate`
- Dataset names:
  - `regShoDaily` (production): data `/data/group/otcMarket/name/regShoDaily`, metadata `/metadata/group/otcMarket/name/regShoDaily`
    - Available fields: `tradeReportDate`, `securitiesInformationProcessorSymbolIdentifier`, `shortParQuantity`, `shortExemptParQuantity`, `totalParQuantity`, `marketCode`, `reportingFacilityCode`
  - `regShoDailyMock` (mock): data `/data/group/otcMarket/name/regShoDailyMock`, metadata `/metadata/group/otcMarket/name/regShoDailyMock`
    - Available fields: `tradeReportDate`, `securitiesInformationProcessorSymbolIdentifier`, `shortParQuantity`, `shortExemptParQuantity`, `totalParQuantity`, `marketCode`, `reportingFacilityCode`

### Threshold List (`thresholdList`)

- Dataset group: `otcMarket`
- Description: OTC Regulation SHO and Rule 4320 Threshold Securities.
- Documentation: https://developer.finra.org/docs#query_api-equity-threshold_list
- Endpoint pattern: `/data/group/otcMarket/name/{dataset}`
- Metadata endpoint: `/metadata/group/otcMarket/name/{dataset}`
- Partition fields: `tradeDate`
- Dataset names:
  - `thresholdList` (production): data `/data/group/otcMarket/name/thresholdList`, metadata `/metadata/group/otcMarket/name/thresholdList`
    - Available fields: `tradeDate`, `issueSymbolIdentifier`, `issueName`, `marketClassCode`, `thresholdListFlag`, `marketCategoryDescription`, `regShoThresholdFlag`, `rule4320Flag`
  - `thresholdListMock` (mock): data `/data/group/otcMarket/name/thresholdListMock`, metadata `/metadata/group/otcMarket/name/thresholdListMock`
    - Available fields: `tradeDate`, `issueSymbolIdentifier`, `issueName`, `marketClassCode`, `thresholdListFlag`, `marketCategoryDescription`, `regShoThresholdFlag`, `rule4320Flag`

### Weekly Summary (`weeklySummary`)

- Dataset group: `otcMarket`
- Description: Weekly aggregate trade data for OTC (ATS and non-ATS) trading data for each ATS/firm with trade reporting obligations under FINRA rules. API Explorer (Playground) TEST IT OUT
- Documentation: https://developer.finra.org/docs#query_api-equity-weekly_summary
- Endpoint pattern: `/data/group/otcMarket/name/{dataset}`
- Metadata endpoint: `/metadata/group/otcMarket/name/{dataset}`
- Partition fields: `weekStartDate`, `tierIdentifier`
- Dataset names:
  - `weeklySummary` (production): data `/data/group/otcMarket/name/weeklySummary`, metadata `/metadata/group/otcMarket/name/weeklySummary`
    - Available fields: `issueSymbolIdentifier`, `issueName`, `firmCRDNumber`, `MPID`, `marketParticipantName`, `tierIdentifier`, `tierDescription`, `summaryStartDate`, `totalWeeklyTradeCount`, `totalWeeklyShareQuantity`, `productTypeCode`, `summaryTypeCode`, `weekStartDate`, `lastUpdateDate`, `initialPublishedDate`, `lastReportedDate`, `totalNotionalSum`
  - `weeklySummaryMock` (mock): data `/data/group/otcMarket/name/weeklySummaryMock`, metadata `/metadata/group/otcMarket/name/weeklySummaryMock`
    - Available fields: `issueSymbolIdentifier`, `issueName`, `firmCRDNumber`, `MPID`, `marketParticipantName`, `tierIdentifier`, `tierDescription`, `summaryStartDate`, `totalWeeklyTradeCount`, `totalWeeklyShareQuantity`, `productTypeCode`, `summaryTypeCode`, `weekStartDate`, `lastUpdateDate`, `initialPublishedDate`, `lastReportedDate`
  - `weeklySummaryHistoric` (historic): data `/data/group/otcMarket/name/weeklySummaryHistoric`, metadata `/metadata/group/otcMarket/name/weeklySummaryHistoric`
    - Available fields: `issueSymbolIdentifier`, `issueName`, `firmCRDNumber`, `MPID`, `marketParticipantName`, `tierIdentifier`, `tierDescription`, `summaryStartDate`, `totalWeeklyTradeCount`, `totalWeeklyShareQuantity`, `productTypeCode`, `summaryTypeCode`, `weekStartDate`, `lastUpdateDate`, `initialPublishedDate`, `lastReportedDate`, `totalNotionalSum`

## FINRA Content (`finra`)

### FINRA Rulebook (`finraRulebook`)

- Dataset group: `finra`
- Description: FINRA's current and historical rules and regulations API Explorer (Playground) TEST IT OUT
- Documentation: https://developer.finra.org/docs#query_api-finra_content-finra_rulebook
- Endpoint pattern: `/data/group/finra/name/{dataset}`
- Metadata endpoint: `/metadata/group/finra/name/{dataset}`
- Partition fields: `ruleNumber`
- Dataset names:
  - `finraRulebook` (production): data `/data/group/finra/name/finraRulebook`, metadata `/metadata/group/finra/name/finraRulebook`
    - Available fields: `ruleNumber`, `effectiveStartDate`, `effectiveEndDate`, `ruleTextAscii`, `ruleTextHtml`, `ruleTitle`, `rulebookHierarchy`, `summaryTopics`, `detailedTopics`
  - `finraRulebookMock` (mock): data `/data/group/finra/name/finraRulebookMock`, metadata `/metadata/group/finra/name/finraRulebookMock`
    - Available fields: `ruleNumber`, `effectiveStartDate`, `effectiveEndDate`, `ruleTextAscii`, `ruleTextHtml`, `ruleTitle`, `rulebookHierarchy`, `summaryTopics`, `detailedTopics`

### Industry Snapshot: Firm Registration Types (`industrySnapshotFirmsByRegistrationType`)

- Dataset group: `finra`
- Description: Breakdown of securities industry registered firms by type of registration.
- Documentation: https://developer.finra.org/docs#query_api-finra_content-industry_snapshot_firm_registration_types
- Endpoint pattern: `/data/group/finra/name/{dataset}`
- Metadata endpoint: `/metadata/group/finra/name/{dataset}`
- Partition fields: `reportDate`
- Dataset names:
  - `industrySnapshotFirmsByRegistrationType` (production): data `/data/group/finra/name/industrySnapshotFirmsByRegistrationType`, metadata `/metadata/group/finra/name/industrySnapshotFirmsByRegistrationType`
    - Available fields: `year`, `individualOrFirm`, `registrationTypeAtEndOfYear`, `numberOfFirms`, `reportDate`
  - `industrySnapshotFirmsByRegistrationTypeMock` (mock): data `/data/group/finra/name/industrySnapshotFirmsByRegistrationTypeMock`, metadata `/metadata/group/finra/name/industrySnapshotFirmsByRegistrationTypeMock`
    - Available fields: `year`, `individualOrFirm`, `registrationTypeAtEndOfYear`, `numberOfFirms`, `reportDate`

## Firm (`firm`)

### 4530 Customer Complaints (`4530filings`)

- Dataset group: `firm`
- Description: 4530 customer complaint filings submitted by your firm. API Explorer (Playground) TEST IT OUT
- Documentation: https://developer.finra.org/docs#query_api-firm-4530_customer_complaints
- Endpoint pattern: `/data/group/firm/name/{dataset}`
- Metadata endpoint: `/metadata/group/firm/name/{dataset}`
- Dataset names:
  - `4530filings` (production): data `/data/group/firm/name/4530filings`, metadata `/metadata/group/firm/name/4530filings`
    - Available fields: `filingNumber`, `versionNumber`, `filingTypeCode`, `filingStatus`, `firmSequenceNumber`, `submissionDate`, `firmCrdNumber`, `eventCode`, `allegedActivityPeriodDate1`, `allegedActivityPeriodDateFlag1`, `allegedActivityPeriodDate2`, `allegedActivityPeriodDateFlag2`, `discoveryDate`, `complaintRelatedToRepresentativeFlag`, `complaintRelatedToFirmFlag`, `complaintRelatedToAffiliateFlag`, `complaintRelatedToOtherFlag`, `complaintRelatedToAccountsPayableFlag`, `complaintRelatedToMunicipalFlag`, `branchCrdNumber`, `branchStateCode`, `representativeCrdNumber`, `representativeCity`, `representativeEmploymentStateCode`, `representativeZipCodeNumber` (+36 more)
  - `4530filingsMock` (mock): data `/data/group/firm/name/4530filingsMock`, metadata `/metadata/group/firm/name/4530filingsMock`
    - Available fields: `filingNumber`, `versionNumber`, `filingTypeCode`, `filingStatus`, `firmSequenceNumber`, `submissionDate`, `firmCrdNumber`, `eventCode`, `allegedActivityPeriodDate1`, `allegedActivityPeriodDateFlag1`, `allegedActivityPeriodDate2`, `allegedActivityPeriodDateFlag2`, `discoveryDate`, `complaintRelatedToRepresentativeFlag`, `complaintRelatedToFirmFlag`, `complaintRelatedToAffiliateFlag`, `complaintRelatedToOtherFlag`, `complaintRelatedToAccountsPayableFlag`, `complaintRelatedToMunicipalFlag`, `branchCrdNumber`, `branchStateCode`, `representativeCrdNumber`, `representativeCity`, `representativeEmploymentStateCode`, `representativeZipCodeNumber` (+36 more)

### Firm Disclosures (`firmDisclosures`)

- Dataset group: `firm`
- Description: Firm disclosure information.
- Documentation: https://developer.finra.org/docs#query_api-registration-firm_disclosures
- Endpoint pattern: `/data/group/firm/name/{dataset}`
- Metadata endpoint: `/metadata/group/firm/name/{dataset}`
- Primary id field: `firmCrdNumber`
- Dataset names:
  - `firmDisclosures` (production): data `/data/group/firm/name/firmDisclosures`, metadata `/metadata/group/firm/name/firmDisclosures`
    - Available fields: `firmCrdNumber`, `disclosures.disclosureType`, `disclosures.occurrenceNumber`, `disclosures.reportableFlag`, `disclosures.disclosableFlag`, `disclosures.archivedFlag`, `disclosures.eventDate`, `registrations.regulatorCode`
  - `firmDisclosuresMock` (mock): data `/data/group/firm/name/firmDisclosuresMock`, metadata `/metadata/group/firm/name/firmDisclosuresMock`
    - Available fields: `firmCrdNumber`, `disclosures.disclosureType`, `disclosures.occurrenceNumber`, `disclosures.reportableFlag`, `disclosures.disclosableFlag`, `disclosures.archivedFlag`, `disclosures.eventDate`, `registrations.regulatorCode`

### Firm Profile (`firmProfile`)

- Dataset group: `firm`
- Description: Basic information about a firm. API Explorer (Playground) TEST IT OUT
- Documentation: https://developer.finra.org/docs#query_api-registration-firm_profile
- Endpoint pattern: `/data/group/firm/name/{dataset}`
- Metadata endpoint: `/metadata/group/firm/name/{dataset}`
- Primary id field: `firmCrdNumber`
- Dataset names:
  - `firmProfile` (production): data `/data/group/firm/name/firmProfile`, metadata `/metadata/group/firm/name/firmProfile`
    - Available fields: `firmCrdNumber`, `doingBusinessAsName`, `firmApplicantName`, `registeredFirmTypeCode`, `sec802FirmIdentifier`, `sec801FirmIdentifier`, `sec8FirmIdentifier`, `firmFinraDistrict`, `firmAddress.addressLine1`, `firmAddress.addressLine2`, `firmAddress.cityName`, `firmAddress.stateCode`, `firmAddress.stateName`, `firmAddress.countryCode`, `firmAddress.countryName`, `firmAddress.postalCode`, `registrations.regulatorCode`
  - `firmProfileMock` (mock): data `/data/group/firm/name/firmProfileMock`, metadata `/metadata/group/firm/name/firmProfileMock`
    - Available fields: `firmCrdNumber`, `doingBusinessAsName`, `firmApplicantName`, `registeredFirmTypeCode`, `sec802FirmIdentifier`, `sec801FirmIdentifier`, `sec8FirmIdentifier`, `firmFinraDistrict`, `firmAddress.addressLine1`, `firmAddress.addressLine2`, `firmAddress.cityName`, `firmAddress.stateCode`, `firmAddress.stateName`, `firmAddress.countryCode`, `firmAddress.countryName`, `firmAddress.postalCode`, `registrations.regulatorCode`

### Firm Registration Status History (`firmRegistrationStatusHistory`)

- Dataset group: `firm`
- Description: A complete listing of registration notices for a firm.
- Documentation: https://developer.finra.org/docs#query_api-registration-firm_registration_status_history
- Endpoint pattern: `/data/group/firm/name/{dataset}`
- Metadata endpoint: `/metadata/group/firm/name/{dataset}`
- Primary id field: `firmCrdNumber`
- Dataset names:
  - `firmRegistrationStatusHistory` (production): data `/data/group/firm/name/firmRegistrationStatusHistory`, metadata `/metadata/group/firm/name/firmRegistrationStatusHistory`
    - Available fields: `firmCrdNumber`, `registrationStatusHistory.regulatorCode`, `registrationStatusHistory.regulatorName`, `registrationStatusHistory.noticeDate`, `registrationStatusHistory.noticeReason`, `registrationStatusHistory.statusName`, `registrationStatusHistory.statusCode`
  - `firmRegistrationStatusHistoryMock` (mock): data `/data/group/firm/name/firmRegistrationStatusHistoryMock`, metadata `/metadata/group/firm/name/firmRegistrationStatusHistoryMock`
    - Available fields: `firmCrdNumber`, `registrationStatusHistory.regulatorCode`, `registrationStatusHistory.regulatorName`, `registrationStatusHistory.noticeDate`, `registrationStatusHistory.noticeReason`, `registrationStatusHistory.statusName`, `registrationStatusHistory.statusCode`

### Firm Registrations (`firmRegistrations`)

- Dataset group: `firm`
- Description: Firm registration information API Explorer (Playground) TEST IT OUT
- Documentation: https://developer.finra.org/docs#query_api-registration-firm_registrations
- Endpoint pattern: `/data/group/firm/name/{dataset}`
- Metadata endpoint: `/metadata/group/firm/name/{dataset}`
- Primary id field: `firmCrdNumber`
- Dataset names:
  - `firmRegistrations` (production): data `/data/group/firm/name/firmRegistrations`, metadata `/metadata/group/firm/name/firmRegistrations`
    - Available fields: `firmCrdNumber`, `registrations.regulatorCode`, `registrations.regulatorName`, `registrations.registrationType`, `registrations.statusName`, `registrations.statusCode`, `registrations.effectiveDate`, `registrations.isCurrent`
  - `firmRegistrationsMock` (mock): data `/data/group/firm/name/firmRegistrationsMock`, metadata `/metadata/group/firm/name/firmRegistrationsMock`
    - Available fields: `firmCrdNumber`, `registrations.regulatorCode`, `registrations.regulatorName`, `registrations.registrationType`, `registrations.statusName`, `registrations.statusCode`, `registrations.effectiveDate`, `registrations.isCurrent`

## Fixed Income (`fixedIncomeMarket`)

### Agency Debt Market Breadth (`agencyMarketBreadth`)

- Dataset group: `fixedIncomeMarket`
- Description: Market breadth calculations for Agency debt securities. API Explorer (Playground) TEST IT OUT
- Documentation: https://developer.finra.org/docs#query_api-fixed_income-agency_debt_market_breadth
- Endpoint pattern: `/data/group/fixedIncomeMarket/name/{dataset}`
- Metadata endpoint: `/metadata/group/fixedIncomeMarket/name/{dataset}`
- Partition fields: `tradeReportDate`
- Dataset names:
  - `agencyMarketBreadth` (production): data `/data/group/fixedIncomeMarket/name/agencyMarketBreadth`, metadata `/metadata/group/fixedIncomeMarket/name/agencyMarketBreadth`
    - Available fields: `tradeReportDate`, `productCategory`, `totalTrades`, `advances`, `declines`, `unchanged`, `fiftyTwoWeekHigh`, `fiftyTwoWeekLow`, `totalVolume`
  - `agencyMarketBreadthMock` (mock): data `/data/group/fixedIncomeMarket/name/agencyMarketBreadthMock`, metadata `/metadata/group/fixedIncomeMarket/name/agencyMarketBreadthMock`
    - Available fields: `tradeReportDate`, `productCategory`, `totalTrades`, `advances`, `declines`, `unchanged`, `fiftyTwoWeekHigh`, `fiftyTwoWeekLow`, `totalVolume`

### Agency Debt Market Sentiment (`agencyMarketSentiment`)

- Dataset group: `fixedIncomeMarket`
- Description: Market sentiment calculations for Agency debt securities.
- Documentation: https://developer.finra.org/docs#query_api-fixed_income-agency_debt_market_sentiment
- Endpoint pattern: `/data/group/fixedIncomeMarket/name/{dataset}`
- Metadata endpoint: `/metadata/group/fixedIncomeMarket/name/{dataset}`
- Partition fields: `tradeReportDate`
- Dataset names:
  - `agencyMarketSentiment` (production): data `/data/group/fixedIncomeMarket/name/agencyMarketSentiment`, metadata `/metadata/group/fixedIncomeMarket/name/agencyMarketSentiment`
    - Available fields: `tradeReportDate`, `tradeType`, `productCategory`, `totalTransactions`, `totalTrades`, `totalVolume`
  - `agencyMarketSentimentMock` (mock): data `/data/group/fixedIncomeMarket/name/agencyMarketSentimentMock`, metadata `/metadata/group/fixedIncomeMarket/name/agencyMarketSentimentMock`
    - Available fields: `tradeReportDate`, `tradeType`, `productCategory`, `totalTransactions`, `totalTrades`, `totalVolume`

### Corporate 144A Debt Market Breadth (`corporate144AMarketBreadth`)

- Dataset group: `fixedIncomeMarket`
- Description: Market breadth calculations for Rule 144A corporate debt securities.
- Documentation: https://developer.finra.org/docs#query_api-fixed_income-corporate_144a_debt_market_breadth
- Endpoint pattern: `/data/group/fixedIncomeMarket/name/{dataset}`
- Metadata endpoint: `/metadata/group/fixedIncomeMarket/name/{dataset}`
- Partition fields: `tradeReportDate`
- Dataset names:
  - `corporate144AMarketBreadth` (production): data `/data/group/fixedIncomeMarket/name/corporate144AMarketBreadth`, metadata `/metadata/group/fixedIncomeMarket/name/corporate144AMarketBreadth`
    - Available fields: `tradeReportDate`, `productCategory`, `totalTrades`, `advances`, `declines`, `unchanged`, `fiftyTwoWeekHigh`, `fiftyTwoWeekLow`, `totalVolume`
  - `corporate144AMarketBreadthMock` (mock): data `/data/group/fixedIncomeMarket/name/corporate144AMarketBreadthMock`, metadata `/metadata/group/fixedIncomeMarket/name/corporate144AMarketBreadthMock`
    - Available fields: `tradeReportDate`, `productCategory`, `totalTrades`, `advances`, `declines`, `unchanged`, `fiftyTwoWeekHigh`, `fiftyTwoWeekLow`, `totalVolume`

### Corporate 144A Debt Market Sentiment (`corporate144AMarketSentiment`)

- Dataset group: `fixedIncomeMarket`
- Description: Market sentiment calculations for Rule 144A corporate debt securities. API Explorer (Playground) TEST IT OUT
- Documentation: https://developer.finra.org/docs#query_api-fixed_income-corporate_144a_debt_market_sentiment
- Endpoint pattern: `/data/group/fixedIncomeMarket/name/{dataset}`
- Metadata endpoint: `/metadata/group/fixedIncomeMarket/name/{dataset}`
- Partition fields: `tradeReportDate`
- Dataset names:
  - `corporate144AMarketSentiment` (production): data `/data/group/fixedIncomeMarket/name/corporate144AMarketSentiment`, metadata `/metadata/group/fixedIncomeMarket/name/corporate144AMarketSentiment`
    - Available fields: `tradeReportDate`, `tradeType`, `productCategory`, `totalTransactions`, `totalTrades`, `totalVolume`
  - `corporate144AMarketSentimentMock` (mock): data `/data/group/fixedIncomeMarket/name/corporate144AMarketSentimentMock`, metadata `/metadata/group/fixedIncomeMarket/name/corporate144AMarketSentimentMock`
    - Available fields: `tradeReportDate`, `tradeType`, `productCategory`, `totalTransactions`, `totalTrades`, `totalVolume`

### Corporate And Agency Capped Volume (`corporatesAndAgenciesCappedVolume`)

- Dataset group: `fixedIncomeMarket`
- Description: Capped volume calculations for corporate and agency debt.
- Documentation: https://developer.finra.org/docs#query_api-fixed_income-corporate_and_agency_capped_volume
- Endpoint pattern: `/data/group/fixedIncomeMarket/name/{dataset}`
- Metadata endpoint: `/metadata/group/fixedIncomeMarket/name/{dataset}`
- Partition fields: `tradeReportDate`
- Dataset names:
  - `corporatesAndAgenciesCappedVolume` (production): data `/data/group/fixedIncomeMarket/name/corporatesAndAgenciesCappedVolume`, metadata `/metadata/group/fixedIncomeMarket/name/corporatesAndAgenciesCappedVolume`
    - Available fields: `tradeReportDate`, `tradeMonth`, `tradeYear`, `gradeCode`, `144AFlag`, `totalTradeCount`, `totalVolumeQuantity`, `parLessThan5MillionQuantity`, `parGreaterThan5MillionLessThan10MillionQuantity`, `parGreaterThan10MillionLessThan25MillionQuantity`, `parGreaterThan25MillionQuantity`, `tradeLessThan5MillionCount`, `tradeGreaterThan5MillionLessThan10MillionCount`, `tradeGreaterThan10MillionLessThan25MillionCount`, `tradeGreaterThan25MillionCount`, `parMaturityLessThan5YearsQuantity`, `tradeMaturityLessThan5YearsCount`, `parMaturityGreaterThan5YearsLessThan10YearsQuantity`, `tradeMaturityGreaterThan5YearsLessThan10YearsCount`, `parMaturityGreaterThan10YearsLessThan25YearsQuantity`, `tradeMaturityGreaterThan10YearsLessThan25YearsCount`, `parMaturityGreaterThan25YearsQuantity`, `tradeMaturityGreaterThan25YearsCount`, `customerBuyParLessThan5YearsQuantity`, `customerBuyTradeMaturityLessThan5YearsCount` (+22 more)
  - `corporatesAndAgenciesCappedVolumeMock` (mock): data `/data/group/fixedIncomeMarket/name/corporatesAndAgenciesCappedVolumeMock`, metadata `/metadata/group/fixedIncomeMarket/name/corporatesAndAgenciesCappedVolumeMock`
    - Available fields: `tradeReportDate`, `tradeMonth`, `tradeYear`, `gradeCode`, `144AFlag`, `totalTradeCount`, `totalVolumeQuantity`, `parLessThan5MillionQuantity`, `parGreaterThan5MillionLessThan10MillionQuantity`, `parGreaterThan10MillionLessThan25MillionQuantity`, `parGreaterThan25MillionQuantity`, `tradeLessThan5MillionCount`, `tradeGreaterThan5MillionLessThan10MillionCount`, `tradeGreaterThan10MillionLessThan25MillionCount`, `tradeGreaterThan25MillionCount`, `parMaturityLessThan5YearsQuantity`, `tradeMaturityLessThan5YearsCount`, `parMaturityGreaterThan5YearsLessThan10YearsQuantity`, `tradeMaturityGreaterThan5YearsLessThan10YearsCount`, `parMaturityGreaterThan10YearsLessThan25YearsQuantity`, `tradeMaturityGreaterThan10YearsLessThan25YearsCount`, `parMaturityGreaterThan25YearsQuantity`, `tradeMaturityGreaterThan25YearsCount`, `customerBuyParLessThan5YearsQuantity`, `customerBuyTradeMaturityLessThan5YearsCount` (+22 more)

### Corporate Debt Market Breadth (`corporateMarketBreadth`)

- Dataset group: `fixedIncomeMarket`
- Description: Market breadth calculations for corporate debt securities.
- Documentation: https://developer.finra.org/docs#query_api-fixed_income-corporate_debt_market_breadth
- Endpoint pattern: `/data/group/fixedIncomeMarket/name/{dataset}`
- Metadata endpoint: `/metadata/group/fixedIncomeMarket/name/{dataset}`
- Partition fields: `tradeReportDate`
- Dataset names:
  - `corporateMarketBreadth` (production): data `/data/group/fixedIncomeMarket/name/corporateMarketBreadth`, metadata `/metadata/group/fixedIncomeMarket/name/corporateMarketBreadth`
    - Available fields: `tradeReportDate`, `productCategory`, `totalTrades`, `advances`, `declines`, `unchanged`, `fiftyTwoWeekHigh`, `fiftyTwoWeekLow`, `totalVolume`
  - `corporateMarketBreadthMock` (mock): data `/data/group/fixedIncomeMarket/name/corporateMarketBreadthMock`, metadata `/metadata/group/fixedIncomeMarket/name/corporateMarketBreadthMock`
    - Available fields: `tradeReportDate`, `productCategory`, `totalTrades`, `advances`, `declines`, `unchanged`, `fiftyTwoWeekHigh`, `fiftyTwoWeekLow`, `totalVolume`

### Corporate Debt Market Sentiment (`corporateMarketSentiment`)

- Dataset group: `fixedIncomeMarket`
- Description: Market sentiment calculations for corporate debt securities.
- Documentation: https://developer.finra.org/docs#query_api-fixed_income-corporate_debt_market_sentiment
- Endpoint pattern: `/data/group/fixedIncomeMarket/name/{dataset}`
- Metadata endpoint: `/metadata/group/fixedIncomeMarket/name/{dataset}`
- Partition fields: `tradeReportDate`
- Dataset names:
  - `corporateMarketSentiment` (production): data `/data/group/fixedIncomeMarket/name/corporateMarketSentiment`, metadata `/metadata/group/fixedIncomeMarket/name/corporateMarketSentiment`
    - Available fields: `tradeReportDate`, `tradeType`, `productCategory`, `totalTransactions`, `totalTrades`, `totalVolume`
  - `corporateMarketSentimentMock` (mock): data `/data/group/fixedIncomeMarket/name/corporateMarketSentimentMock`, metadata `/metadata/group/fixedIncomeMarket/name/corporateMarketSentimentMock`
    - Available fields: `tradeReportDate`, `tradeType`, `productCategory`, `totalTransactions`, `totalTrades`, `totalVolume`

### Securitized Product Capped Volume (`securitizedProductsCappedVolume`)

- Dataset group: `fixedIncomeMarket`
- Description: Capped volume calculations for securitized products. API Explorer (Playground) TEST IT OUT
- Documentation: https://developer.finra.org/docs#query_api-fixed_income-securitized_product_capped_volume
- Endpoint pattern: `/data/group/fixedIncomeMarket/name/{dataset}`
- Metadata endpoint: `/metadata/group/fixedIncomeMarket/name/{dataset}`
- Partition fields: `tradeReportDate`
- Dataset names:
  - `securitizedProductsCappedVolume` (production): data `/data/group/fixedIncomeMarket/name/securitizedProductsCappedVolume`, metadata `/metadata/group/fixedIncomeMarket/name/securitizedProductsCappedVolume`
    - Available fields: `tradeReportDate`, `tradeMonth`, `tradeYear`, `productType`, `securitySubtype`, `averageTransactionCount`
  - `securitizedProductsCappedVolumeMock` (mock): data `/data/group/fixedIncomeMarket/name/securitizedProductsCappedVolumeMock`, metadata `/metadata/group/fixedIncomeMarket/name/securitizedProductsCappedVolumeMock`
    - Available fields: `tradeReportDate`, `tradeMonth`, `tradeYear`, `productType`, `securitySubtype`, `averageTransactionCount`

### Treasury Daily Aggregates (`treasuryDailyAggregates`)

- Dataset group: `fixedIncomeMarket`
- Description: Daily trading volume in US Treasury Securities reported to TRACE.
- Documentation: https://developer.finra.org/docs#query_api-fixed_income-treasury_daily_aggregates
- Endpoint pattern: `/data/group/fixedIncomeMarket/name/{dataset}`
- Metadata endpoint: `/metadata/group/fixedIncomeMarket/name/{dataset}`
- Partition fields: `tradeDate`
- Dataset names:
  - `treasuryDailyAggregates` (production): data `/data/group/fixedIncomeMarket/name/treasuryDailyAggregates`, metadata `/metadata/group/fixedIncomeMarket/name/treasuryDailyAggregates`
    - Available fields: `tradeDate`, `productCategory`, `yearsToMaturity`, `benchmark`, `atsInterdealerCount`, `atsInterdealerVolume`, `dealerCustomerCount`, `dealerCustomerVolume`, `volumeWeightedAveragePrice`
  - `treasuryDailyAggregatesMock` (mock): data `/data/group/fixedIncomeMarket/name/treasuryDailyAggregatesMock`, metadata `/metadata/group/fixedIncomeMarket/name/treasuryDailyAggregatesMock`
    - Available fields: `tradeDate`, `productCategory`, `yearsToMaturity`, `benchmark`, `atsInterdealerCount`, `atsInterdealerVolume`, `dealerCustomerCount`, `dealerCustomerVolume`, `volumeWeightedAveragePrice`

### Treasury Monthly Aggregates (`treasuryMonthlyAggregates`)

- Dataset group: `fixedIncomeMarket`
- Description: Monthly trading volume in US Treasury Securities reported to TRACE.
- Documentation: https://developer.finra.org/docs#query_api-fixed_income-treasury_monthly_aggregates
- Endpoint pattern: `/data/group/fixedIncomeMarket/name/{dataset}`
- Metadata endpoint: `/metadata/group/fixedIncomeMarket/name/{dataset}`
- Partition fields: `beginningOfTheMonthDate`
- Dataset names:
  - `treasuryMonthlyAggregates` (production): data `/data/group/fixedIncomeMarket/name/treasuryMonthlyAggregates`, metadata `/metadata/group/fixedIncomeMarket/name/treasuryMonthlyAggregates`
    - Available fields: `beginningOfTheMonthDate`, `productCategory`, `yearsToMaturity`, `benchmark`, `atsInterdealerCount`, `atsInterdealerVolume`, `dealerCustomerCount`, `dealerCustomerVolume`
  - `treasuryMonthlyAggregatesMock` (mock): data `/data/group/fixedIncomeMarket/name/treasuryMonthlyAggregatesMock`, metadata `/metadata/group/fixedIncomeMarket/name/treasuryMonthlyAggregatesMock`
    - Available fields: `beginningOfTheMonthDate`, `productCategory`, `yearsToMaturity`, `benchmark`, `atsInterdealerCount`, `atsInterdealerVolume`, `dealerCustomerCount`, `dealerCustomerVolume`

## Registration (`registration`)

### Accounting (`accounting`)

- Dataset group: `registration`
- Description: Provides accounting transactions for a given date range.
- Documentation: https://developer.finra.org/docs#query_api-registration-accounting
- Endpoint pattern: `/data/group/registration/name/{dataset}`
- Metadata endpoint: `/metadata/group/registration/name/{dataset}`
- Dataset names:
  - `accounting` (production): data `/data/group/registration/name/accounting`, metadata `/metadata/group/registration/name/accounting`; notes: HTTP 400
    - Available fields: not discoverable in the unauthenticated generation run; call metadata with authorized credentials.
  - `accountingMock` (mock): data `/data/group/registration/name/accountingMock`, metadata `/metadata/group/registration/name/accountingMock`; notes: HTTP 400
    - Available fields: not discoverable in the unauthenticated generation run; call metadata with authorized credentials.

### Altered SSN and DOB (`alteredSSNandDOB`)

- Dataset group: `registration`
- Description: Get altered identifiers of registered individuals in the QA Test Environment.
- Documentation: https://developer.finra.org/docs#query_api-registration-altered_ssn_and_dob
- Endpoint pattern: `/data/group/registration/name/{dataset}`
- Metadata endpoint: `/metadata/group/registration/name/{dataset}`
- Dataset names:
  - `alteredSSNandDOB` (production): data `/data/group/registration/name/alteredSSNandDOB`, metadata `/metadata/group/registration/name/alteredSSNandDOB`; notes: HTTP 404
    - Available fields: not discoverable in the unauthenticated generation run; call metadata with authorized credentials.

### Branch Delta (`branchDelta`)

- Dataset group: `registration`
- Description: The dataset provides the ability to identify firm's branches whose information has changed within a given datetime range.
- Documentation: https://developer.finra.org/docs#query_api-registration-branch_delta
- Endpoint pattern: `/data/group/registration/name/{dataset}`
- Metadata endpoint: `/metadata/group/registration/name/{dataset}`
- Dataset names:
  - `branchDelta` (production): data `/data/group/registration/name/branchDelta`, metadata `/metadata/group/registration/name/branchDelta`; notes: HTTP 400
    - Available fields: not discoverable in the unauthenticated generation run; call metadata with authorized credentials.
  - `branchDeltaMock` (mock): data `/data/group/registration/name/branchDeltaMock`, metadata `/metadata/group/registration/name/branchDeltaMock`; notes: HTTP 400
    - Available fields: not discoverable in the unauthenticated generation run; call metadata with authorized credentials.

### Branch List (`branchList`)

- Dataset group: `registration`
- Description: Provides a list of active branches for a calling FIRM.
- Documentation: https://developer.finra.org/docs#query_api-registration-branch_list
- Endpoint pattern: `/data/group/registration/name/{dataset}`
- Metadata endpoint: `/metadata/group/registration/name/{dataset}`
- Dataset names:
  - `branchList` (production): data `/data/group/registration/name/branchList`, metadata `/metadata/group/registration/name/branchList`; notes: HTTP 400
    - Available fields: not discoverable in the unauthenticated generation run; call metadata with authorized credentials.
  - `branchListMock` (mock): data `/data/group/registration/name/branchListMock`, metadata `/metadata/group/registration/name/branchListMock`; notes: HTTP 400
    - Available fields: not discoverable in the unauthenticated generation run; call metadata with authorized credentials.

### Broker Dealer Firm List (`brokerDealerFirmList`)

- Dataset group: `registration`
- Description: This dataset contains information about all broker-dealer firms that are registered with and regulated by FINRA.
- Documentation: https://developer.finra.org/docs#query_api-registration-broker_dealer_firm_list_
- Endpoint pattern: `/data/group/registration/name/{dataset}`
- Metadata endpoint: `/metadata/group/registration/name/{dataset}`
- Dataset names:
  - `brokerDealerFirmList` (production): data `/data/group/registration/name/brokerDealerFirmList`, metadata `/metadata/group/registration/name/brokerDealerFirmList`; notes: HTTP 400
    - Available fields: not discoverable in the unauthenticated generation run; call metadata with authorized credentials.
  - `brokerDealerFirmListMock` (mock): data `/data/group/registration/name/brokerDealerFirmListMock`, metadata `/metadata/group/registration/name/brokerDealerFirmListMock`; notes: HTTP 400
    - Available fields: not discoverable in the unauthenticated generation run; call metadata with authorized credentials.

### Composite Branch (`compositeBranch`)

- Dataset group: `registration`
- Description: Provides comprehensive real-time data that FINRA has for a given Branch CRD.
- Documentation: https://developer.finra.org/docs#query_api-registration-composite_branch
- Endpoint pattern: `/data/group/registration/name/{dataset}`
- Metadata endpoint: `/metadata/group/registration/name/{dataset}`
- Dataset names:
  - `compositeBranch` (production): data `/data/group/registration/name/compositeBranch`, metadata `/metadata/group/registration/name/compositeBranch`; notes: HTTP 400
    - Available fields: not discoverable in the unauthenticated generation run; call metadata with authorized credentials.
  - `compositeBranchMock` (mock): data `/data/group/registration/name/compositeBranchMock`, metadata `/metadata/group/registration/name/compositeBranchMock`; notes: HTTP 400
    - Available fields: not discoverable in the unauthenticated generation run; call metadata with authorized credentials.

### Composite Individual (`compositeIndividual`)

- Dataset group: `registration`
- Description: Delivers comprehensive real-time data that FINRA has for a given Individual CRD number. API Explorer (Playground) TEST IT OUT
- Documentation: https://developer.finra.org/docs#query_api-registration-composite_individual
- Endpoint pattern: `/data/group/registration/name/{dataset}`
- Metadata endpoint: `/metadata/group/registration/name/{dataset}`
- Dataset names:
  - `compositeIndividual` (production): data `/data/group/registration/name/compositeIndividual`, metadata `/metadata/group/registration/name/compositeIndividual`; notes: HTTP 400
    - Available fields: not discoverable in the unauthenticated generation run; call metadata with authorized credentials.
  - `compositeIndividualMock` (mock): data `/data/group/registration/name/compositeIndividualMock`, metadata `/metadata/group/registration/name/compositeIndividualMock`; notes: HTTP 400
    - Available fields: not discoverable in the unauthenticated generation run; call metadata with authorized credentials.

### Composite Individual Seed (`compositeindividualseed`)

- Dataset group: `registration`
- Description: Provides a JSON file download via API of all the individuals currently employed by the requesting firm and individuals terminated within the last 30 calendar days.
- Documentation: https://developer.finra.org/docs#query_api-registration-composite_individual_seed
- Endpoint pattern: `/data/group/registration/name/{dataset}`
- Metadata endpoint: `/metadata/group/registration/name/{dataset}`
- Dataset names:
  - `compositeindividualseed` (production): data `/data/group/registration/name/compositeindividualseed`, metadata `/metadata/group/registration/name/compositeindividualseed`; notes: HTTP 404
    - Available fields: not discoverable in the unauthenticated generation run; call metadata with authorized credentials.

### Individual Delta (`individualDelta`)

- Dataset group: `registration`
- Description: The dataset provides the ability to identify individual representatives whose information has changed within a given date and time range.
- Documentation: https://developer.finra.org/docs#query_api-registration-individual_delta
- Endpoint pattern: `/data/group/registration/name/{dataset}`
- Metadata endpoint: `/metadata/group/registration/name/{dataset}`
- Dataset names:
  - `individualDelta` (production): data `/data/group/registration/name/individualDelta`, metadata `/metadata/group/registration/name/individualDelta`; notes: HTTP 400
    - Available fields: not discoverable in the unauthenticated generation run; call metadata with authorized credentials.
  - `individualDeltaMock` (mock): data `/data/group/registration/name/individualDeltaMock`, metadata `/metadata/group/registration/name/individualDeltaMock`; notes: HTTP 400
    - Available fields: not discoverable in the unauthenticated generation run; call metadata with authorized credentials.

### Individual Fingerprint (`fingerprint`)

- Dataset group: `registration`
- Description: Delivers comprehensive real-time fingerprint data that FINRA has for a given Individual.
- Documentation: https://developer.finra.org/docs#query_api-registration-individual_fingerprint
- Endpoint pattern: `/data/group/registration/name/{dataset}`
- Metadata endpoint: `/metadata/group/registration/name/{dataset}`
- Dataset names:
  - `fingerprint` (production): data `/data/group/registration/name/fingerprint`, metadata `/metadata/group/registration/name/fingerprint`; notes: HTTP 404
    - Available fields: not discoverable in the unauthenticated generation run; call metadata with authorized credentials.
  - `fingerprintMock` (mock): data `/data/group/registration/name/fingerprintMock`, metadata `/metadata/group/registration/name/fingerprintMock`; notes: HTTP 404
    - Available fields: not discoverable in the unauthenticated generation run; call metadata with authorized credentials.

### Individual Pre-Registration Search (`preRegistrationIndividual`)

- Dataset group: `registration`
- Description: Access the registration records of industry individuals being considered for employment. API Explorer (Playground) TEST IT OUT
- Documentation: https://developer.finra.org/docs#query_api-registration-individual_pre_registration_search
- Endpoint pattern: `/data/group/registration/name/{dataset}`
- Metadata endpoint: `/metadata/group/registration/name/{dataset}`
- Dataset names:
  - `preRegistrationIndividual` (production): data `/data/group/registration/name/preRegistrationIndividual`, metadata `/metadata/group/registration/name/preRegistrationIndividual`
    - Available fields: `individualCrdNumber`, `firstName`, `middleName`, `lastName`, `suffixName`, `statutoryDisqualificationCode`, `militaryDeferredFlag`, `statutoryDisqualificationStatusDate`, `personalInformation.countryOfBirthCode`, `personalInformation.stateOfBirthCode`, `personalInformation.stateProvinceOfBirthCode`, `disclosures.occurrenceNumber`, `disclosures.disclosureTypeCode`, `disclosures.reportableFlag`, `disclosures.publiclyDisclosableFlag`, `disclosures.archiveReasonType`, `disclosures.questionAnsweredText`, `disclosures.eventDate`, `disclosureFilings.eventDate`, `disclosureFilings.formTypeCode`, `disclosureFilings.filingNumber`, `disclosureFilings.filingDate`, `disclosureFilings.filedByRegulatorCode`, `disclosureFilings.filedByFirmCrdNumber`, `disclosureFilings.occurrenceNumber` (+121 more)
  - `preRegistrationIndividualMock` (mock): data `/data/group/registration/name/preRegistrationIndividualMock`, metadata `/metadata/group/registration/name/preRegistrationIndividualMock`
    - Available fields: `individualCrdNumber`, `firstName`, `middleName`, `lastName`, `suffixName`, `statutoryDisqualificationCode`, `militaryDeferredFlag`, `statutoryDisqualificationStatusDate`, `personalInformation.countryOfBirthCode`, `personalInformation.stateOfBirthCode`, `personalInformation.stateProvinceOfBirthCode`, `disclosures.occurrenceNumber`, `disclosures.disclosureTypeCode`, `disclosures.reportableFlag`, `disclosures.publiclyDisclosableFlag`, `disclosures.archiveReasonType`, `disclosures.questionAnsweredText`, `disclosures.eventDate`, `disclosureFilings.eventDate`, `disclosureFilings.formTypeCode`, `disclosureFilings.filingNumber`, `disclosureFilings.filingDate`, `disclosureFilings.filedByRegulatorCode`, `disclosureFilings.filedByFirmCrdNumber`, `disclosureFilings.occurrenceNumber` (+121 more)

### Individual Pre-Registration Search v2 (`preRegistrationIndividualv2`)

- Dataset group: `registration`
- Description: Access the registration records of individuals in the industry being considered for employment, along with complete disclosure information. Retirement Date: February 26, 2027 Replaced by: U4FormPrefill
- Documentation: https://developer.finra.org/docs#query_api-registration-individual_pre_registration_search_v2
- Endpoint pattern: `/data/group/registration/name/{dataset}`
- Metadata endpoint: `/metadata/group/registration/name/{dataset}`
- Dataset names:
  - `preRegistrationIndividualv2` (production): data `/data/group/registration/name/preRegistrationIndividualv2`, metadata `/metadata/group/registration/name/preRegistrationIndividualv2`
    - Available fields: `dateOfBirth`, `individualCrdNumber`, `drpTermination.200905.drpIdentifierDetails.disclosureIdentifier`, `drpTermination.200905.drpIdentifierDetails.occurrenceIdentifier`, `drpTermination.200905.drpIdentifierDetails.filingIdentifier`, `drpTermination.200905.reportableFlag`, `drpTermination.200905.formU4Termination.terminationAllegation`, `drpTermination.200905.formU4Termination.employingFirmName`, `drpTermination.200905.formU4Termination.productTypeOtherText`, `drpTermination.200905.formU4Termination.terminationTypeCode`, `drpTermination.200905.formU4Termination.disclosureEventDateDetails.date`, `drpTermination.200905.formU4Termination.disclosureEventDateDetails.exactDate`, `drpTermination.200905.formU4Termination.disclosureEventDateDetails.dateExplanation`, `drpTermination.200905.formU4Termination.terminationU4DisclosureQuestionSelection`, `drpTermination.200905.formU4Termination.commentText`, `drpTermination.200905.formU4Termination.productType`, `drpTermination.200905.disclosureVersion`, `drpTermination.200905.id`, `drpTermination.200905.baseline`, `drpTermination.200905.discloseToPublicFlag`, `drpTermination.200510.drpIdentifierDetails.disclosureIdentifier`, `drpTermination.200510.drpIdentifierDetails.occurrenceIdentifier`, `drpTermination.200510.drpIdentifierDetails.filingIdentifier`, `drpTermination.200510.reportableFlag`, `drpTermination.200510.formU4Termination.terminationAllegation` (+867 more)
  - `preRegistrationIndividualv2Mock` (mock): data `/data/group/registration/name/preRegistrationIndividualv2Mock`, metadata `/metadata/group/registration/name/preRegistrationIndividualv2Mock`
    - Available fields: `dateOfBirth`, `individualCrdNumber`, `drpTermination.200905.drpIdentifierDetails.disclosureIdentifier`, `drpTermination.200905.drpIdentifierDetails.occurrenceIdentifier`, `drpTermination.200905.drpIdentifierDetails.filingIdentifier`, `drpTermination.200905.reportableFlag`, `drpTermination.200905.formU4Termination.terminationAllegation`, `drpTermination.200905.formU4Termination.employingFirmName`, `drpTermination.200905.formU4Termination.productTypeOtherText`, `drpTermination.200905.formU4Termination.terminationTypeCode`, `drpTermination.200905.formU4Termination.disclosureEventDateDetails.date`, `drpTermination.200905.formU4Termination.disclosureEventDateDetails.exactDate`, `drpTermination.200905.formU4Termination.disclosureEventDateDetails.dateExplanation`, `drpTermination.200905.formU4Termination.terminationU4DisclosureQuestionSelection`, `drpTermination.200905.formU4Termination.commentText`, `drpTermination.200905.formU4Termination.productType`, `drpTermination.200905.disclosureVersion`, `drpTermination.200905.id`, `drpTermination.200905.baseline`, `drpTermination.200905.discloseToPublicFlag`, `drpTermination.200510.drpIdentifierDetails.disclosureIdentifier`, `drpTermination.200510.drpIdentifierDetails.occurrenceIdentifier`, `drpTermination.200510.drpIdentifierDetails.filingIdentifier`, `drpTermination.200510.reportableFlag`, `drpTermination.200510.formU4Termination.terminationAllegation` (+867 more)

### Individual Registration Validation (`registrationValidationIndividual`)

- Dataset group: `registration`
- Description: Validate the registration status of a registered individual with FINRA and the states independent of what firm they are affiliated with. API Explorer (Playground) TEST IT OUT
- Documentation: https://developer.finra.org/docs#query_api-registration-individual_registration_validation
- Endpoint pattern: `/data/group/registration/name/{dataset}`
- Metadata endpoint: `/metadata/group/registration/name/{dataset}`
- Primary id field: `individualCrdNumber`
- Dataset names:
  - `registrationValidationIndividual` (production): data `/data/group/registration/name/registrationValidationIndividual`, metadata `/metadata/group/registration/name/registrationValidationIndividual`
    - Available fields: `individualCrdNumber`, `firstName`, `middleName`, `lastName`, `suffixName`, `employments.firmCrdNumber`, `employments.doingBusinessAsName`, `employments.isActive`, `registrations.regulatorName`, `registrations.isInactiveOrSuspended`, `registrations.regScope`, `registrations.regDate`, `registrations.status`, `registrations.categories`
  - `registrationValidationIndividualMock` (mock): data `/data/group/registration/name/registrationValidationIndividualMock`, metadata `/metadata/group/registration/name/registrationValidationIndividualMock`
    - Available fields: `individualCrdNumber`, `firstName`, `middleName`, `lastName`, `suffixName`, `employments.firmCrdNumber`, `employments.doingBusinessAsName`, `employments.isActive`, `registrations.regulatorName`, `registrations.isInactiveOrSuspended`, `registrations.regScope`, `registrations.regDate`, `registrations.status`, `registrations.categories`

### Individual Registration Validation Details (`IndividualRegistrationValidationDetails`)

- Dataset group: `registration`
- Description: Validate the registration status including disclosure details of a registered individual with FINRA and the states independent of what firm they are affiliated with.
- Documentation: https://developer.finra.org/docs#query_api-registration-individual_registration_validation_details
- Endpoint pattern: `/data/group/registration/name/{dataset}`
- Metadata endpoint: `/metadata/group/registration/name/{dataset}`
- Primary id field: `individualCrdNumber`
- Dataset names:
  - `IndividualRegistrationValidationDetails` (production): data `/data/group/registration/name/IndividualRegistrationValidationDetails`, metadata `/metadata/group/registration/name/IndividualRegistrationValidationDetails`
  - `IndividualRegistrationValidationDetailsMock` (mock): data `/data/group/registration/name/IndividualRegistrationValidationDetailsMock`, metadata `/metadata/group/registration/name/IndividualRegistrationValidationDetailsMock`

### Registered Individual Search (`RegisteredIndividualSearch`)

- Dataset group: `registration`
- Description: Access CRD Numbers for registered individuals. API Explorer (Playground) TEST IT OUT
- Documentation: https://developer.finra.org/docs#query_api-registration-registered_individual_search
- Endpoint pattern: `/data/group/registration/name/{dataset}`
- Metadata endpoint: `/metadata/group/registration/name/{dataset}`
- Dataset names:
  - `RegisteredIndividualSearch` (production): data `/data/group/registration/name/RegisteredIndividualSearch`, metadata `/metadata/group/registration/name/RegisteredIndividualSearch`
    - Available fields: `individualCrdNumber`, `lastName`, `firstName`
  - `RegisteredIndividualSearchMock` (mock): data `/data/group/registration/name/RegisteredIndividualSearchMock`, metadata `/metadata/group/registration/name/RegisteredIndividualSearchMock`
    - Available fields: `individualCrdNumber`, `lastName`, `firstName`

### U4 Form Prefill (`U4FormPrefill`)

- Dataset group: `registration`
- Description: The U4 Form Prefill dataset can be used to prepopulate Form U4 Initial fields when submitting registration applications through the Submission API.
- Documentation: https://developer.finra.org/docs#query_api-registration-u4_form_prefill
- Endpoint pattern: `/data/group/registration/name/{dataset}`
- Metadata endpoint: `/metadata/group/registration/name/{dataset}`
- Dataset names:
  - `U4FormPrefill` (production): data `/data/group/registration/name/U4FormPrefill`, metadata `/metadata/group/registration/name/U4FormPrefill`; notes: HTTP 500
    - Available fields: not discoverable in the unauthenticated generation run; call metadata with authorized credentials.
