START:
    LOADI R0, #0xC0 ; load lower byte
    LUI R0, #0x01 ; load upper byte - creates #0x01C0

    LOADI R1, #0x01 ; load shift amount of 1
    LUI R1, #0x80 ; sets our most significant bit
   
    SHFT R2, R0, R1 ;
    ADDI R1, R1, #0x1 ;
    SHFT R3, R0, R1 ;
    ADDI R1, R1, #0x1 ;
    SHFT R4, R0, R1 ;
    ADDI R1, R1, #0x1 ;
    SHFT R5, R0, R1 ;
    ADDI R1, R1, #0x1 ;
    SHFT R6, R0, R1 ;
    ADDI R1, R1, #0x1 ; R1 = #0x8006 - last operand used
    SHFT R7, R0, R1 ;

    HALT ;
