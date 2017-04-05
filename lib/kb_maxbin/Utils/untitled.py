        upload_message = ''
        with open('MaxBin_test/test_result/out_header.summary', 'r') as summary_file:
            first_line = True
            lines = summary_file.readlines()
            print lines
            for line in lines:
                if first_line:
                    line_list = line.split('\t')
                    upload_message += line_list[0] + 2 * '\t' + line_list[1] + '\t'
                    upload_message += line_list[2] + '\t' + line_list[3] + '\t' + line_list[4]
                    first_line = False
                else:
                    line_list = line.split('\t')
                    upload_message += line_list[0] + '\t' + line_list[1] + 2 * '\t'
                    upload_message += line_list[2] + 2 * '\t' + line_list[3] + 2 * '\t'
                    upload_message += line_list[4]

        print upload_message