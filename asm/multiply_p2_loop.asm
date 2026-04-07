START:
    LOADI R0, #5 ; the original constant operand, 5 - antiquated from non-looping assembly
    LOADI R1, #1 ; load the shift amount used, 1
    LOADI R2, #5 ; the computed value to be stored into memory
    LOADI R3, #0 ; the base memory address to be written to (0x0000)
    LOADI R4, #9 ; loop counter
    CALL LOOP 

LOOP:
    SHFT R2, R2, R1 ;
    STORE R2, [R3 + #0] ; store computer value in R3
    ADDI R3, R3, #1 ; increment our memory location
    SUB R4, R4, R1 ; decrement our loop counter
    BNE LOOP

    HALT ;

