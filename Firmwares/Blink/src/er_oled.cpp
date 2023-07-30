#include <SPI.h>
#include "er_oled.h"

void command(uint8_t cmd){
    digitalWrite(OLED_DC, LOW);
    SPIWrite(&cmd, 1);
}

void SPIWrite(uint8_t *buffer, int bufferLength) {
    int i;
    for (i = 0; i < bufferLength; i++) {
        SPI.transfer(buffer[i]);
    }
}

void er_oled_begin()
{

    pinMode(OLED_RST, OUTPUT);
    pinMode(OLED_DC, OUTPUT);
    pinMode(OLED_CS, OUTPUT);
    SPI.begin();
    
    SPI.setClockDivider(SPI_CLOCK_DIV128);
    
    digitalWrite(OLED_CS, LOW);
    digitalWrite(OLED_RST, HIGH);
    delay(10);
    digitalWrite(OLED_RST, LOW);
    delay(10);
    digitalWrite(OLED_RST, HIGH);
    
    command(0xae);//--turn off oled panel
	
    command(0xd5);//--set display clock divide ratio/oscillator frequency
    command(0x80);//--set divide ratio

    command(0xa8);//--set multiplex ratio
    command(0x27);//--1/40 duty

    command(0xd3);//-set display offset
    command(0x00);//-not offset

    command(0xad);//--Internal IREF Setting	
    command(0x30);//--

    command(0x8d);//--set Charge Pump enable/disable
    command(0x14);//--set(0x10) disable

    command(0x40);//--set start line address

    command(0xa6);//--set normal display

    command(0xa4);//Disable Entire Display On

    command(0xa1);//--set segment re-map 128 to 0

    command(0xC8);//--Set COM Output Scan Direction 64 to 0

    command(0xda);//--set com pins hardware configuration
    command(0x12);

    command(0x81);//--set contrast control register
    command(0xaf);

    command(0xd9);//--set pre-charge period
    command(0x22);

    command(0xdb);//--set vcomh
    command(0x20);

    command(0xaf);//--turn on oled panel

}

void er_oled_clear(uint8_t* buffer)
{
	int i;
	for(i = 0;i < WIDTH * HEIGHT / 8;i++)
	{
		buffer[i] = 0;
	}
}

void er_oled_pixel(int x, int y, char color, uint8_t* buffer)
{
    if(x > WIDTH || y > HEIGHT)return ;
    if(color)
        buffer[x+(y/8)*WIDTH] |= 1<<(y%8);
    else
        buffer[x+(y/8)*WIDTH] &= ~(1<<(y%8));
}


void er_oled_char(unsigned char x, unsigned char y, char acsii, char size, char mode, uint8_t* buffer)
{
    unsigned char i, j, y0=y;
    char temp;
    unsigned char ch = acsii - ' ';
    for(i = 0;i<size;i++) {
        if(mode)temp = pgm_read_byte(&Font1206[ch][i]);
        else temp = ~pgm_read_byte(&Font1206[ch][i]);
        for(j =0;j<8;j++)
        {
            if(temp & 0x80) er_oled_pixel(x, y, 1, buffer);
            else er_oled_pixel(x, y, 0, buffer);
            temp <<= 1;
            y++;
            if((y-y0) == size)
            {
                y = y0;
                x++;
                break;
            }
        }
    }
}

void er_oled_string(uint8_t x, uint8_t y, const char *pString, uint8_t Size, uint8_t Mode, uint8_t* buffer)
{
    while (*pString != '\0') {       
        if (x > (WIDTH - Size / 2)) {
            x = 0;
            y += Size;
            if (y > (HEIGHT - Size)) {
                y = x = 0;
            }
        }
        
        er_oled_char(x, y, *pString, Size, Mode, buffer);
        x += Size / 2;
        pString++;
    }
}


void er_oled_display(uint8_t* pBuf)
{    uint8_t page,i;   
    for (page = 0; page < PAGES; page++) {         
        command(0xB0 + page);/* set page address */     
        command(0x0c);   /* set low column address */      
        command(0x11);  /* set high column address */      
        //digitalWrite(OLED_DC, HIGH);
        //SPIWrite(pBuf, WIDTH); /* write data  one page*/
        //pBuf += WIDTH;        
        for(i = 0; i< WIDTH; i++ ) {
          digitalWrite(OLED_DC, HIGH);
          SPIWrite(pBuf, 1);// write data one
          *pBuf++;
        }        
    }
}
