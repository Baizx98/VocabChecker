def process_vocabulary(
    variant_file, cet6_file, output_file, notfound_file, debug=False
):
    """
    处理词汇表，生成包含原始单词及其变体的输出文件，以及未找到的单词列表。

    参数：
        variant_file (str): 包含单词变体信息的文件路径。
        cet6_file (str): 包含CET6词汇表的文件路径。
        output_file (str): 输出文件路径。
        notfound_file (str): 未找到的单词输出文件路径。
    """

    # 读取单词变体信息
    variant_map = {}
    with open(variant_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split("->")
                if len(parts) == 2:
                    original_with_num, variants = parts
                    # 去掉原始单词后面的 /数字 部分
                    original_word = original_with_num.split("/")[
                        0
                    ].strip()  # 去掉空白符
                    variant_list = [
                        v.strip() for v in variants.split(",")
                    ]  # 去掉变体中的空白符
                    variant_map[original_word] = [original_word] + variant_list

    # 读取CET6词汇表
    cet6_words = []
    with open(cet6_file, "r", encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            if word:
                cet6_words.append(word)

    # 生成输出和未找到的单词列表
    not_found_words = []
    with open(output_file, "w", encoding="utf-8") as f_out:
        for word in cet6_words:
            if word in variant_map:
                variants = variant_map[word]
                for variant in variants:
                    f_out.write(variant + "\n")
            else:
                f_out.write(word + "\n")
                not_found_words.append(word)

    if debug:
        # 将未找到的单词写入文件
        with open(notfound_file, "w", encoding="utf-8") as f_notfound:
            for word in not_found_words:
                f_notfound.write(word + "\n")


if __name__ == "__main__":
    # 示例用法
    variant_file = "./vocab/lemma.en.txt"  # 包含单词变体信息的文件
    cet6_file = "./vocab/CET6_vocab_20250228.txt"  # 包含CET6词汇表的文件
    output_file = "output_words.txt"  # 输出文件
    notfound_file = "notfound.txt"  # 未找到的单词输出文件

    process_vocabulary(variant_file, cet6_file, output_file, notfound_file)
