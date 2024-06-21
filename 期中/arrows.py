def string_with_arrows(text, start_pos, end_pos):
    result = ''

    line_start_idx = max(text.rfind('\n', 0, start_pos.idx), 0)
    line_end_idx = text.find('\n', line_start_idx + 1)
    if line_end_idx < 0: line_end_idx = len(text)
    
    total_lines = end_pos.line - start_pos.line + 1
    for i in range(total_lines):
        line = text[line_start_idx:line_end_idx]
        start_col = start_pos.col if i == 0 else 0
        end_col = end_pos.col if i == total_lines - 1 else len(line) - 1

        result += line + '\n'
        result += ' ' * start_col + '^' * (end_col - start_col)

        line_start_idx = line_end_idx
        line_end_idx = text.find('\n', line_start_idx + 1)
        if line_end_idx < 0: line_end_idx = len(text)

    return result.replace('\t', '')