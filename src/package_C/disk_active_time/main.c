#include <pdh.h>
#include <stdio.h>

PDH_HQUERY hQuery;      // 查询句柄
PDH_HCOUNTER hCounter;  // 计数器句柄
PDH_FMT_COUNTERVALUE counterValue;

double get() {
    PdhCollectQueryData(hQuery);
    PdhGetFormattedCounterValue(hCounter, PDH_FMT_DOUBLE, 0, &counterValue);
    return counterValue.doubleValue;
}

void start() {
    // 后面加上 != ERROR_SUCCESS 判断有没有成功
    PdhOpenQuery(NULL, 0, &hQuery);
    PdhAddCounter(hQuery, "\\PhysicalDisk(_Total)\\% Disk Time", 0, &hCounter);  // 性能监视器/PhysicalDisk
}

void end() {
    PdhRemoveCounter(hCounter);
    PdhCloseQuery(hQuery);
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
