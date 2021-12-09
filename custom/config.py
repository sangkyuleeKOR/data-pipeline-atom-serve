
PLC_INFORM = {
    'host':"192.168.1.10",
    'port':2004
}

# collect_save_img : stream중에 원본사진을 저장한다.
# collect_crop_img : stream중에 crop한 이미지를 저장한다.
# collect_count : 저장할 원본사진의 수, -1이면 unlimit이다.
COLLECT_OPTION = {
    'collect_cycle' : 0.48,
    'collect_count' : 1000,
    'collect_save_img' :True,
    'collect_save_img_path' : 'img_save/',
    'collect_save_crop_img' :False,
    'collect_save_crop_img_path' : 'crop_img_save/',
    'width' : (210,530)
}

# mode : none, 테스크를 실행하지 않는다.
# mode : jump, 6번째 슬롯부터 한칸씩 건너서 불량으로 인식한다.
# mode : delay, 6번째 슬롯부터 한칸씩 건너서 delay시킨다.
TEST_OPTION = {
    'mode' : 'none',
    'delay_time' : 0.5
}

CLOUD_OPTION = {
    'broker_address' : '220.93.184.42',
    'broker_port' : 50005,
    'true_product_period': 1 
}

INFERENCE_OPTION = {
    'inference-process' : True

}
