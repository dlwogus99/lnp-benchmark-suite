# Benchmark card

## Goal

LNP 조성과 payload 특성으로 transfection percentage를 예측하는 회귀 pipeline을 비교한다.

## Protocol

- group: `study_id`
- validation: leave-one-study-out
- metrics: MAE, R²
- models: train mean, standardized kNN, ridge regression

## Demo data

24개 합성 formulation, 6개 가상 study. 공개 연구에서 자주 쓰는 조성 컬럼과
10–1929 nt payload size 범위를 반영했지만 원 논문의 측정값을 복제하지 않았다.

## Limitations

작은 합성 데이터의 metric은 모델 성능 주장에 사용할 수 없다. 실제 비교에서는
assay, cell line, route, dose, study provenance를 공변량 또는 계층으로 다뤄야 한다.
