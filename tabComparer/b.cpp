#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
using namespace std;

bool handleFile(ifstream &inFile, vector<string> &tab) {
	tab.clear();
	string s;
	while (getline(inFile, s)) {
		while (s.back() == '\n' || s.back() == '\r')
			s.pop_back();
		tab.emplace_back(s);
	}
	if (tab.empty() || tab[0].empty()) {
		cerr << "Empty file or line; ";
		return 0;
	}
	for (auto &i : tab)
		if (i.size() != tab[0].size()) {
			cerr << "Different size between lines; ";
			return 0;
		}
	for (int i = 0, cnt; i < (int)tab[0].size(); i += cnt) {
		if (tab.back()[i] <= '0' || tab.back()[i] > '9') {
			cerr << "Wrong format type 1 in the last line; ";
			return 0;
		}
		cnt = tab.back()[i] - '0';
		if (cnt == 1) {
			for (int j = 0; j < (int)tab.size() - 1; ++j)
				if ((tab[j][i] == '|') != (tab[0][i] == '|')) {
					cerr << "Seperate bars in wrong format; ";
					return 0;
				}
		}
		else {
			for (int j = 0; j < cnt; ++j) {
				if (j > 0 && (i + j >= (int)tab.back().size() || tab.back()[i + j] != ' ')) {
					cerr << "Wrong format tyep 2 in the last line; ";
					return 0;
				}
				for (int k = 0; k < (int)tab.size() - 1; ++k)
					if (tab[k][i + j] == '|') {
						cerr << "Wrong format type 3 in the last line; \n";
						return 0;
					}
			}
		}
	}
	if (tab[0][0] == '|' || tab[0].back() != '|') {
		cerr << "First or last column in wrong format; ";
		return 0;
	}
	return 1;
}

void segComp(vector<string> &tb1, vector<string> &tb2, int l1, int r1, int l2, int r2, int &totCnt1, int &totCnt2, int &okCnt, int &numOkCnt) {
	totCnt1 = totCnt2 = okCnt = numOkCnt = 0;
	for (int i = l1; i < r1; ++i)
		if ('0' < tb1.back()[i] && tb1.back()[i] <= '9')
			++totCnt1;
	for (int i = l2; i < r2; ++i)
		if ('0' < tb2.back()[i] && tb2.back()[i] <= '9')
			++totCnt2;
	if (totCnt1 != totCnt2)
		return;

	for (int i1 = l1, i2 = l2, cnt1, cnt2; i1 < r1; i1 += cnt1, i2 += cnt2) {
		cnt1 = tb1.back()[i1] - '0';
		cnt2 = tb2.back()[i2] - '0';
		bool ok = 1, numOk = 1;
		for (int j = 0; j < (int)tb1.size() - 1; ++j) {
			string s1 = "", s2 = "";
			for (int k = 0; k < cnt1; ++k)
				s1 += tb1[j][i1 + k];
			for (int k = 0; k < cnt2; ++k)
				s2 += tb2[j][i2 + k];
			while (!s1.empty() && s1.back() == '-')
				s1.pop_back();
			reverse(s1.begin(), s1.end());
			while (!s1.empty() && s1.back() == '-')
				s1.pop_back();
			reverse(s1.begin(), s1.end());
			while (!s2.empty() && s2.back() == '-')
				s2.pop_back();
			reverse(s2.begin(), s2.end());
			while (!s2.empty() && s2.back() == '-')
				s2.pop_back();
			reverse(s2.begin(), s2.end());
			if (s1 != s2) ok = 0;
			while (!s1.empty() && (0 > s1.back() || s1.back() > '9'))
				s1.pop_back();
			reverse(s1.begin(), s1.end());
			while (!s1.empty() && (0 > s1.back() || s1.back() > '9'))
				s1.pop_back();
			reverse(s1.begin(), s1.end());
			while (!s2.empty() && (0 > s2.back() || s2.back() > '9'))
				s2.pop_back();
			reverse(s2.begin(), s2.end());
			while (!s2.empty() && (0 > s2.back() || s2.back() > '9'))
				s2.pop_back();
			reverse(s2.begin(), s2.end());
			if (s1 != s2) numOk = 0;
		}
		if (ok) ++okCnt;
		if (numOk) ++numOkCnt;
	}
}

void tabComp(vector<string> &tb1, vector<string> &tb2, int &segCnt1, int &segCnt2, int &totCnt, int &okCnt, int &numOkCnt, int &okSegCnt, int &numOkSegCnt) {
	vector<int> sep1(1, -1), sep2(1, -1);
	for (int i = 0; i < (int)tb1[0].size(); ++i)
		if (tb1[0][i] == '|')
			sep1.emplace_back(i);
	for (int i = 0; i < (int)tb2[0].size(); ++i)
		if (tb2[0][i] == '|')
			sep2.emplace_back(i);
	segCnt1 = (int)sep1.size() - 1;
	segCnt2 = (int)sep2.size() - 1;
	totCnt = okCnt = numOkCnt = okSegCnt = numOkSegCnt = 0;
	for (int i = 1; i < min((int)sep1.size(), (int)sep2.size()); ++i) {
		int tot1, tot2, ok, numOk;
		segComp(tb1, tb2, sep1[i - 1] + 1, sep1[i], sep2[i - 1] + 1, sep2[i], tot1, tot2, ok, numOk);
		totCnt += min(tot1, tot2);
		okCnt += ok, numOkCnt += numOk;
		if (ok == tot1)
			++okSegCnt;
		if (numOk == tot1)
			++numOkSegCnt;
	}
}

int main(int argc, char* argv[]) {
	if (argc < 3) {
		cerr << "Usage: " << argv[0] << " <input file 1> <input file 2>\n";
		return 1;
	}
	
	string file1 = argv[1], file2 = argv[2];
	ifstream inFile1(file1), inFile2(file2);
	if (!inFile1) {
		cerr << "Error: Could not open file " << file1 << '\n';
		return 1;
	}
	if (!inFile2) {
		cerr << "Error: Could not open file " << file2 << '\n';
		return 1;
	}

	vector<string> tab1, tab2;
	if (!handleFile(inFile1, tab1)) {
		cerr << "Error: Incorrect format in file " << file1 << '\n';
		return 1;
	}
	if (!handleFile(inFile2, tab2)) {
		cerr << "Error: Incorrect format in file " << file2 << '\n';
		return 1;
	}
	if (tab1.size() != tab2.size()) {
		cerr << "Error: Different format between two files\n";
		return 1;
	}

	int seg1, seg2, tot, ok, numOk, okSeg, numOkSeg;
	tabComp(tab1, tab2, seg1, seg2, tot, ok, numOk, okSeg, numOkSeg);

	cout << "Comparison ended successfully\n";
	cout << "File 1: " << seg1 << " bars\n";
	cout << "File 2: " << seg2 << " bars\n";
	cout << "Totally correct bar: " << okSeg << " / " << min(seg1, seg2) << '\n';
	cout << "Partially correct bar: " << numOkSeg << " / " << min(seg1, seg2) << '\n';
	cout << "Totally correct sound: " << ok << " / " << tot << '\n';
	cout << "Partially correct sound: " << numOk << " / " << tot << '\n';

	return 0;
}
