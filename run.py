#-*- coding: utf-8 -*-
import api_auto_test.api_test as apitest
if __name__ == "__main__":
    api = apitest.test_run('./config/global_setting.config','api_cardexchange','api_cardexchange_result')
    api.api_run_test_batch()
