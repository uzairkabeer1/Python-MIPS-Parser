import csv
from collections import defaultdict

class Pipeline:
    def execute_instruction(self, instruction, fp_registers, int_registers, memory):
        opcode, *operands = instruction.split()

        if opcode == 'LI':
            register = operands[0]
            value = operands[1] if len(operands) > 1 else 0
            int_registers[register] = int(value)

        elif opcode == 'L.D':
            fp_register = operands[0]
            offset_register = operands[1].split('(')[1][:-1] if len(operands) > 1 else None
            offset = operands[1].split('(')[0] if len(operands) > 1 else '0'
            if offset_register is None:
                address = int(offset)
            else:
                address = int(int_registers[offset_register]) + int(offset)
            fp_registers[fp_register] = memory[address]

        elif opcode == 'ADD.D':
            dest = operands[0]
            src1 = operands[1].split(',')[0] if len(operands) > 1 else 'F0'
            src2 = operands[2] if len(operands) > 2 else 'F0'
            fp_registers[dest] = float(fp_registers[src1]) + float(fp_registers[src2])

        elif opcode == 'S.D':
            src = operands[0]
            offset_register = operands[1].split('(')[1][:-1] if len(operands) > 1 else None
            offset = operands[1].split('(')[0] if len(operands) > 1 else '0'
            if offset_register is None:
                address = int(offset)
            else:
                address = int(int_registers[offset_register]) + int(offset)
            memory[address] = fp_registers[src]

        elif opcode == 'ADDI':
            dest = operands[0]
            src = operands[1] if len(operands) > 1 else None
            immediate = operands[2] if len(operands) > 2 else '0'
            if src is not None:
                int_registers[dest] = int(int_registers[src]) + int(immediate)
            else:
                int_registers[dest] = int(immediate)

        elif opcode == 'BNE':
            reg1 = operands[0] if len(operands) > 0 else None
            reg2 = operands[1] if len(operands) > 1 else None
            label = operands[2] if len(operands) > 2 else None
            if reg1 is not None and reg2 is not None and label is not None:
                if int(int_registers[reg1]) != int(int_registers[reg2]):
                    return label

        return None

    @staticmethod
    def simulate_pipeline(filename):
        with open(filename, 'r') as file:
            instructions = file.readlines()

        fp_registers = {f'F{i}': 0.0 for i in range(32)}
        int_registers = defaultdict(int)
        memory = [0.0] * 1000

        table = []
        current_cycle = 1
        branch_target = None

        for line in instructions:
            line = line.strip()

            if not line or line.startswith('#'):
                continue

            if branch_target:
                instruction = branch_target
                branch_target = None
            else:
                instruction = line.split('#', 1)[0].strip()

            if current_cycle > 1:
                pipeline_stages = [''] * (current_cycle - 2)
            else:
                pipeline_stages = []

            if 'ADD.D' in instruction or 'S.D' in instruction:
                prev_instr = table[-1][0] if table else None
                if prev_instr and ('L.D' in prev_instr or 'ADD.D' in prev_instr or 'S.D' in prev_instr):
                    pipeline_stages.extend(['if', 'id', 'stall', 'stall', 'stall', 'stall', 'A1', 'A2', 'wb'])
                else:
                    pipeline_stages.extend(['if', 'id', 'ex', 'mem', '', '', 'A1', 'A2', 'wb'])
            else:
                pipeline_stages.extend(['if', 'id', 'ex', 'mem', 'wb'])

            table.append([instruction.ljust(18)] + pipeline_stages)

            branch_target = Pipeline().execute_instruction(instruction, fp_registers, int_registers, memory)

            if branch_target:
                instructions = [inst for inst in instructions if not inst.startswith('Loop:')]
                instructions = [inst.strip() for inst in instructions]

            current_cycle += 1

        return table

    @staticmethod
    def save_table_to_csv(table, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(table)

table = Pipeline.simulate_pipeline('input.txt')
if table:
    Pipeline.save_table_to_csv(table, 'pipeline.csv')
    print(f'MIPS Pipeline table saved to "pipeline.csv"')