START:
    LOADI R0, #0xAA ;load first value into R0
    LOADI R1, #0x55 ;load second value into R1
    AND R2, R1, R0 ;check if operation is safe
    BNE TARGET ;branch if it isn't
    OR R2, R1, R0 ;if safe, store the value of R1 OR R0 in R2
    HALT

TARGET:
    LOADI R2, #0x0 ;if not safe, store the value 0 in R2
    HALT