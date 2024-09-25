import unit.common as common


common = common.CommonClassify()
GT_path = r"/data/FAW_HAD/datalists/tlr/train.json"
common.read_ground_true_datalist(GT_path)

predict_result_path = r"/data/had_total_issue_torch_latest_model_test/TLR_total_datalist_infer/Test_240919_tlr_base_v1.6.a/results/results.txt"
common.read_predict_result_datalist(predict_result_path)
common.save_resule_data(predict_result_path)