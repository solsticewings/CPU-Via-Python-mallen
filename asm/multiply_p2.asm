START:
    LOADI R0, #0x3 ; the original constant operand, 3
    LOADI R1, #0x1 ; load the shift amount used, 1
    SHFT R2, R0, R1 ; 3 x 2^1
    ADDI R1, R1, #0x1
    SHFT R3, R0, R1 ; 3 x 2^2
    ADDI R1, R1, #0x1
    SHFT R4, R0, R1 ; 3 x 2^3
    ADDI R1, R1, #0x1
    SHFT R5, R0, R1 ; 3 x 2^4
    ADDI R1, R1, #0x1
    SHFT R6, R0, R1 ; 3 x 2^5
    ADDI R1, R1, #0x1
    SHFT R7, R0, R1 ; 3 x 2^6
    HALT ;