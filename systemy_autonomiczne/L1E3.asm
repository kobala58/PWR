#include <p16f877a.inc>
__CONFIG _FOSC_EXTRC & _WDTE_OFF & _PWRTE_OFF & _BOREN_OFF & _LVP_ON & _CPD_OFF & _WRT_OFF & _CP_OFF
RES_VECT CODE 0x0000
goto START
MAIN_PROG CODE

START
    DCounter1 EQU 0X30
    DCounter2 EQU 0X31
    DCounter3 EQU 0X32
    bcf STATUS, RP1
    bsf STATUS, RP0
    
    movlw 0x00
    movwf TRISA ;nastaw 
    movlw 0xFF
    movwf TRISC
    bcf STATUS, RP0
    movlw b'00011111'
    movwf PORTA


LOOP
    MOVLW 0X07
    MOVWF DCounter1
    MOVLW 0X03
    MOVWF DCounter2
    MOVLW 0X02
    MOVWF DCounter3
    CALL LOOP1
    CALL SWITCH
    GOTO LOOP

LOOP1
    DECFSZ DCounter1, 1
    GOTO LOOP1
    DECFSZ DCounter2, 1
    GOTO LOOP1
    DECFSZ DCounter3, 1
    GOTO LOOP1
;    NOP
    RETURN    

SWITCH
    rlf PORTA,1
    RETURN 

end
