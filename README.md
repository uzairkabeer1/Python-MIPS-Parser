# Python-MIPS-Parser
<a name="br1"></a> 

Project Specification

Deliverables:

You can use one of the following languages to implement the program:

● C

● C++

● Python

● Java

● Verilog

● VHDL

You will also need to:

• Write clean code

• Make sure your code is readable even for someone not versed in the particular language

• Comment your code where necessary (too much commenting of code sometimes makes it hard to

read)

• Submit a user manual for your code detailing how to run it; step by step instructions as well as

what OS to use and how to compile the source code.

• Your instructor has access to the following OS:

• a Mac OS (M1) platform

• a Linux platform

• Windows 10/11

• I would suggest you test your code on one of these platforms to ensure it runs as you expect.

• Make sure that it is possible to run your code without needing to purchase any additional

software. (Trials count as a purchase)

Return a zip file named project.zip containing:

• The program files and source code.

• A text file (README) detailing how to run your simulator and recompile it if needed.

Your program should take as an input a text file with MIPS code (see Instructions section), and

output a table similar to one used in class showing:

**•** When each instruction completed each stage

**•** The values in all the registers at the end of execution

• The values in memory at the end of execution

**•** See input and output sections for further details



<a name="br2"></a> 

Grading:

The code and program will be graded according to the following:

10% -if the program works. It does not have to be perfect for you to get this credit

50%- Implementation

• How close is your simulator to mimicking a true pipeline

• How well does it meet the specifications in this document

• Do values in the register match what is expected

• How does it handle corner cases

40%-Well written code:

• use of good variable names

• code is easy to follow an understand and is well organized

• Good instructions on how to run/compile your code

Processor Configuration:

The algorithm will model a processor with the following configuration:

●

●

●

●

Pipelined FP adder for FP adds and subtracts -2cycles

Pipelined FP multiplier for FP multiplies -10cycles

Pipelined FP divider for FP divides -40cycles

Integer Unit/s for Loads, Stores, Integer Adds and Subtracts -1cycle

32 FP registers and 32 integer registers.

●

All registers will be initialized to 0 at the beginning.

Full forwarding is possible and it is possible to write and read the register in the same cycle.

Control Instructions:

We will assume a non correlating 1 bit predictor (0,1) for the branch instructions in the simulator.

All branches, conditional and unconditional, will assume “taken” to start and the prediction per

branch will be updated when resolved only if it is wrong. Branch resolution will happen in the

execute stage. If the prediction was wrong then all instructions fetched after the branch will seize

execution and the correct instruction will be fetched on the corresponding cycle. The prediction

information should also be updated at this point. If the prediction is correct then the pipeline will

continue execution without any interruptions.



<a name="br3"></a> 

The label for control instructions will always be the first word on the line and end in a colon, for

example: “Loop:”

Data Memory:

The data memory hierarchy will be one level 1 cache and a main memory.

Data memory is not pipelined, thus you cannot have more than one instruction in the mem stage.

L1 Data Cache:

The L1 cache will be empty at the start of the simulator. It will have four sets and will take a direct

mapped approach for block placement and a write back strategy.

Reads from the L1 cache will take 1 cycle for a hit, however, if there is a miss, then a read to main

memory will take 2 cycles for a total of 3 cycles (first cycle for the search in cache and 2 cycles for

search in main memory). In the case of a miss, the data will be brought into the cache in addition to

bringing it into the pipeline.

A miss will lead to stalls.

In addition to data, each block brought into the cache should have information regarding the block’s

original address in main memory. This will be used to track whether blocks exist in the cache for a

hit or miss and where to write the data back.

Main Data Memory:

You can initialize your data memory to the following values:

Memory Location

Value in Memory

0

1

45

12

0

2

3

92

10

135

254

127

18

4

4

5

6

7

8

9

10

55



<a name="br4"></a> 

11

12

13

14

15

16

17

18

8

2

98

13

5

233

158

167

The memory location will be the index of the value and we will use that index as the actual address

for loads and stores.

For simplicity the value at the memory location is what gets loaded into a register and if the memory

location is offset then it loads whatever value is at that offset.

Example:

LD F2, 1(17) would load 167 into register F2

In some cases, the address will come from an integer register for example:

LI $2, 17

LD F2, 0($2)

This sequence would load 158 into register F2. The addresses wrap back around so, address 19 would

be location 0 in main memory.

Instructions:

You can program your algorithm for the following instructions:

Memory Instructions:

L.D Fa, Offset(addr)

Load a floating point value into Fa

Store a floating point value from Fa

Load a 64 bit Integer Immediate into $d

Load an integer value into $d

S.D Fa, Offset(addr)

LI $d, IMM64 -Integer Immediate Load

LW $d, Offset(addr)

SW $s, Offset(addr)

Store an integer from $s

ALU Instructions:

ADD $d, $s, $t - Integer add

$d = $s + $t



<a name="br5"></a> 

ADDI $d, $s, immediate – Integer Add with

$d = $s + immediate

Immediate

ADD.D Fd, Fs, Ft – Floating Point Add

SUB.D Fd, Fs, Ft – Floating Point Subtract

SUB $d, $s, $t -Integer Subtract

Fd = Fs + Ft

Fd = Fs - Ft

$d = $s - $t

Fd = Fs X Ft

Fd = Fs ÷ Ft

\*MUL.D Fd, Fs, Ft -Floating Point Multiply

DIV.D Fd, Fs, Ft – Floating Point Divide

\*You can assume that Fd is big enough to hold the value of the result.

Control Instructions:

BEQ $S, $T, OFF18 - Branch to offset if equal

IF $S = $T, PC += OFF18±

IF $S ≠ $T, PC += OFF18±

PC = PC31:28 :: ADDR28∅

BNE $S, $T, OFF18 - Branch to offset if not equal

J ADDR28 - Unconditional jump to addr

$s/$d/$t are integer registers and Fa/Fd are floating point registers

Inputs

Your program should take the following inputs (how it takes them is up to you):

1\. Text file with a program written using MIPS instructions outlined above

●

You do not have to account for MIPS instructions not outlined in this document

Outputs

Your program should output the following:

1\. The pipeline showing the different stages for the different instructions (similar to how we

have been doing it in class).

○

For the the different execute stages you should use the following:

i.

ii.

iii.

FP ADD/SUB: A# (where # stands for number)

FP DIV: D# (where # stands for number)

FP MUL: M# (where # stands for number)



<a name="br6"></a> 

iv.

Integer Units: E (this includes branches)

2\. Final values in the FP and Integer registers as well as the memory locations.


