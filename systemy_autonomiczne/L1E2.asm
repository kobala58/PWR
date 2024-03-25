#include <p16f877a.inc>
__CONFIG _FOSC_EXTRC & _WDTE_OFF & _PWRTE_OFF & _BOREN_OFF & _LVP_ON & _CPD_OFF & _WRT_OFF & _CP_OFF
RES_VECT CODE 0x0000
goto START
MAIN_PROG CODE

START
    ; CONSTS
    LEDFLAGS equ 0x20
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
    movwf LEDFLAG 
    
LOOP
    btfsc PORTC, 0
    CALL LED1
    btfsc PORTC, 1
    CALL LED2
    btfsc PORTC, 2
    CALL LED3
    btfsc PORTC, 3
    CALL LED4
    
    goto LOOP

LED1
    movlw 0x01
    XORWF LEDFLAG,0
    ; movf LEDFLAG, W
    movwf PORTA
    btfsc PORTC, 0
    goto $-1
    RETURN

LED2
    movlw Ox02
    XORWF LEDFLAG,1
    movf LEDFLAG, W
    movwf PORTA
    btfsc PORTC, 1
    goto $-1
    RETURN
LED3
    movlw 0x04
    XORWF LEDFLAG,1
    movf LEDFLAG, W
    movwf PORTA
    btfsc PORTC, 2
    goto $-1
    RETURN
    
LED4
    movlw 0x08
    XORWF LEDFLAG,1
    movf LEDFLAG, W
    movwf PORTA
    btfsc PORTC, 3
    goto $-1
    RETURN
end
