#ifndef UART_H_
#define UART_H_

void initUART(void);
void transmitData(int data);
unsigned char receiveData(void);

#endif /* UART_H_ */
