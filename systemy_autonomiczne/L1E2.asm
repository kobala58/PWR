#include <p16f877a.inc>
__CONFIG _FOSC_EXTRC & _WDTE_OFF & _PWRTE_OFF & _BOREN_OFF & _LVP_ON & _CPD_OFF & _WRT_OFF & _CP_OFF
RES_VECT CODE 0x0000
goto START
MAIN_PROG CODE

START
    bcf STATUS, RP1
    bsf STATUS, RP0
    movlw 0x00
    movwf TRISA
    movlw 0xFF
    movwf TRISC
    bcf STATUS, RP0
    movlw 0x00
    movwf PORTA

    movlw 0x00
    movwf 0x20
LOOP
    movf PORTC, W
    XORWF 0x20,0
    movf 0x20, W
    movwf PORTA
    goto LOOP
end
