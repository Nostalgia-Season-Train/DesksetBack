#include <pdh.h>
#include <stdio.h>

typedef struct returnData {
    DWORD error;
    double result;
} data;

PDH_HQUERY hQuery = NULL;      // 查询句柄
PDH_HCOUNTER hCounter = NULL;  // 计数器句柄
PDH_FMT_COUNTERVALUE counterValue;

// 注：首次调用返回 0xC0000BC6，后续调用正常
  // 原因：PdhCollectQueryData 首次调用得到的数据无效，
    // 随后 PdhGetFormattedCounterValue 对该无效数据出错 0xC0000BC6
data get() {
    if (hQuery == NULL || hCounter == NULL) {
        data data = { ERROR_SUCCESS, 0.0 };
        return data;
    }

    PDH_STATUS pdhStatus;

    pdhStatus = PdhCollectQueryData(hQuery);
    if (pdhStatus != ERROR_SUCCESS) {
        data data = { pdhStatus, 0.0 };
        return data;
    }

    pdhStatus = PdhGetFormattedCounterValue(hCounter, PDH_FMT_DOUBLE, 0, &counterValue);
    if (pdhStatus != ERROR_SUCCESS) {
        data data = { pdhStatus, 0.0 };
        return data;
    }

    data data = { ERROR_SUCCESS, counterValue.doubleValue };
    return data;
}

DWORD start() {
    PDH_STATUS pdhStatus;  // 实测类型为 unsigned long 跟 DWORD 一致

    pdhStatus = PdhOpenQuery(NULL, 0, &hQuery);
    if (pdhStatus != ERROR_SUCCESS) {
        return pdhStatus;
    }

    pdhStatus = PdhAddCounter(hQuery, "\\PhysicalDisk(_Total)\\% Disk Time", 0, &hCounter);  // 性能监视器/PhysicalDisk
    if (pdhStatus != ERROR_SUCCESS) {
        return pdhStatus;
    }

    return ERROR_SUCCESS;
}

DWORD end() {
    if (hQuery == NULL || hCounter == NULL) {
        return ERROR_SUCCESS;
    }

    PDH_STATUS pdhStatus;

    pdhStatus = PdhRemoveCounter(hCounter);
    if (pdhStatus != ERROR_SUCCESS) {
        return pdhStatus;
    }

    pdhStatus = PdhCloseQuery(hQuery);
    if (pdhStatus != ERROR_SUCCESS) {
        return pdhStatus;
    }

    return ERROR_SUCCESS;
}


/* 测试程序 */
int main() {
    start();
    while (TRUE) {
        printf("磁盘活动时间: %.2f%%\n", get());
        Sleep(1000);
    }
    end();

    return 0;
}
