# coding=utf-8

class LanguageHeadersGenerator():

	def __init__(self, input_filename):
		import codecs
		in_file = codecs.open(input_filename, 'r', encoding='utf-8')
		self.data_matrix = []
		for line in in_file:
			if line.strip() != '':
				self.data_matrix.append(line.strip('\n').split('\t'))
		in_file.close()

		self.row_offset = 1 # Row number where the data begins (row 0 contains titles)


	def create_dicts(self):

		# Finds languages IDs (ISO 639-1) enclosed in brackets 
		lang_id_list = [(i, e[e.find('(')+1:e.find(')')]) for i, e in enumerate(self.data_matrix[0]) if ('(' in e and ')' in e)]

		for lang_element in lang_id_list:
			if lang_element[1] not in iso_639_1_language_ids:
				print "WARNING: Language ID not found in ISO 639-1 list (%s)" % lang_element[1]

		# Get list of Labels from first column
		label_list = [line[0] for line in self.data_matrix[self.row_offset:]]

		for lang_col, lang_id in lang_id_list:
			translations_list = [row[lang_col] for row in self.data_matrix[self.row_offset:]]
			self.export_files(lang_id, zip(label_list, translations_list))


	def export_files(self, lang_id, translations_tuples):
		out_filename = "Language_%2s.h" % lang_id

		out_file = open(out_filename, 'w')

		out_file.write("#ifndef LANGUAGE_%2s_H\n" % lang_id)
		out_file.write("#define LANGUAGE_%2s_H\n" % lang_id)
		out_file.write("\n")
		out_file.write("#include <avr/pgmspace.h>\n")
		out_file.write("\n")

		for key, value in translations_tuples:
			encoded_value = ""
			for c in value:
				try:
					encoded_c = c.encode('ascii')
				except:
					if lang_id == 'RU':
						if repr(c) == "u'\u0410'":
							encoded_c = 'A'
						else:
							encoded_c = '""%s""' % repr(c.encode('iso-8859-5'))[1:-1]
					else:
						encoded_c = '""%s""' % repr(c)[2:-1]
				finally:
					encoded_value += encoded_c

			out_file.write('%-55s = "%s";\n' % ("const char %2s_%s[] PROGMEM" % (lang_id, key), encoded_value))
		
		out_file.write("\n#endif //LANGUAGE_%2s_H" % lang_id)
		out_file.close()

		print "Exported translation file for %2s (%s)" % (lang_id, out_filename)


iso_639_1_language_ids = ['AA', 'AB', 'AF', 'AK', 'SQ', 'AM', 'AR', 'AN', 'HY', 'AS', 'AV', 'AE', 'AY', 'AZ', 'BA', 'BM', 'EU', 'BE', 'BN',\
	'BH', 'BI', 'BO', 'BS', 'BR', 'BG', 'MY', 'CA', 'CS', 'CH', 'CE', 'ZH', 'CU', 'CV', 'KW', 'CO', 'CR', 'CY', 'CS', 'DA', 'DE', 'DV', 'NL',\
	'DZ', 'EL', 'EN', 'EO', 'ET', 'EU', 'EE', 'FO', 'FA', 'FJ', 'FI', 'FR', 'FR', 'FY', 'FF', 'GA', 'DE', 'GD', 'GA', 'GL', 'GV', 'EL', 'GN',\
	'GU', 'HT', 'HA', 'HE', 'HZ', 'HI', 'HO', 'HR', 'HU', 'HY', 'IG', 'IS', 'IO', 'II', 'IU', 'IE', 'IA', 'ID', 'IK', 'IS', 'IT', 'JV', 'JA',\
	'KL', 'KN', 'KS', 'KA', 'KR', 'KK', 'KM', 'KI', 'RW', 'KY', 'KV', 'KG', 'KO', 'KJ', 'KU', 'LO', 'LA', 'LV', 'LI', 'LN', 'LT', 'LB', 'LU',\
	'LG', 'MK', 'MH', 'ML', 'MI', 'MR', 'MS', 'MI', 'MK', 'MG', 'MT', 'MN', 'MI', 'MS', 'MY', 'NA', 'NV', 'NR', 'ND', 'NG', 'NE', 'NL', 'NN',\
	'NB', 'NO', 'OC', 'OJ', 'OR', 'OM', 'OS', 'PA', 'FA', 'PI', 'PL', 'PT', 'PS', 'QU', 'RM', 'RO', 'RO', 'RN', 'RU', 'SG', 'SA', 'SI', 'SK',\
	'SK', 'SL', 'SE', 'SM', 'SN', 'SD', 'SO', 'ST', 'ES', 'SQ', 'SC', 'SR', 'SS', 'SU', 'SW', 'SV', 'TY', 'TA', 'TT', 'TE', 'TG', 'TL', 'TH',\
	'BO', 'TI', 'TO', 'TN', 'TS', 'TK', 'TR', 'TW', 'UG', 'UK', 'UR', 'UZ', 'VE', 'VI', 'VO', 'CY', 'WA', 'WO', 'XH', 'YI', 'YO', 'ZA', 'ZH', 'ZU']

if __name__ == "__main__":
	input_filename = 'Texto de Firmware - Graphic LCD.tsv'
	gen = LanguageHeadersGenerator(input_filename)
	gen.create_dicts()


