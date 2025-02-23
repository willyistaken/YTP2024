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

const int base[] = {64, 59, 55, 50, 45, 40};

void tabStd(vector<string> &tb, vector<vector<string>> &tbAr1, vector<vector<int>> &tbAr2, vector<vector<int>> &tbAr3) {
	tbAr1.clear(), tbAr2.clear(), tbAr3.clear();
	for (int i = 2, cnt; i < (int)tb[0].size(); i += cnt) {
		cnt = tb.back()[i] - '0';
		if (tb[0][i] == '|')
			continue;
		vector<string> c1;
		vector<int> c2, c3;
		for (int j = 0; j < (int)tb.size() - 1; ++j) {
			string s;
			for (int k = 0; k < cnt; ++k)
				s += tb[j][i + k];
			while (!s.empty() && s.back() == '-')
				s.pop_back();
			reverse(s.begin(), s.end());
			while (!s.empty() && s.back() == '-')
				s.pop_back();
			reverse(s.begin(), s.end());
			c1.emplace_back(s);
			while (!s.empty() && ('0' > s.back() || s.back() > '9'))
				s.pop_back();
			reverse(s.begin(), s.end());
			while (!s.empty() && ('0' > s.back() || s.back() > '9'))
				s.pop_back();
			reverse(s.begin(), s.end());
			if (s.empty()) c2.emplace_back(-1);
			else {
				int val = stoi(s);
				c2.emplace_back(val), c3.emplace_back(base[j] + val);
			}
		}
		sort(c3.begin(), c3.end());
		tbAr1.emplace_back(c1), tbAr2.emplace_back(c2), tbAr3.emplace_back(c3);
	}
	while (!tbAr3.empty() && tbAr3.back().empty())
		tbAr1.pop_back(), tbAr2.pop_back(), tbAr3.pop_back();
}

template<typename T>
void tbArComp(vector<T> tbAr1, vector<T> tbAr2, int &cnt, int &clearCnt) {
	vector<int> dp((int)tbAr2.size() + 1, 0), cl = dp;
	for (int i = 0; i < (int)tbAr1.size(); ++i) {
		auto nxt = dp, ncl = cl;
		nxt[0] = i + 1;
		for (int j = 0; j < (int)tbAr2.size(); ++j) {
			if (tbAr1[i] == tbAr2[j]) {
				nxt[j + 1] = dp[j], ncl[j + 1] = cl[j];
				if (tbAr1[i].empty())
					++ncl[j + 1];
			}
			else {
				if (dp[j + 1] < nxt[j])
					nxt[j + 1] = dp[j + 1] + 1, ncl[j + 1] = cl[j + 1];
				else if (dp[j + 1] == nxt[j])
					nxt[j + 1] = dp[j + 1] + 1, ncl[j + 1] = min(cl[j + 1], ncl[j]);
				else nxt[j + 1] = nxt[j] + 1, ncl[j + 1] = ncl[j];
			}
		}
		dp.swap(nxt), cl.swap(ncl);
	}
	cnt = max(tbAr1.size(), tbAr2.size()) - dp.back();
	clearCnt = cl.back();
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

	int seg1 = 1, seg2 = 1, ok, numOk, numCombOk, clear, okSeg, numOkSeg;
	vector<vector<string>> tbAr11, tbAr21;
	vector<vector<int>> tbAr12, tbAr22, tbAr13, tbAr23;
	tabStd(tab1, tbAr11, tbAr12, tbAr13);
	tabStd(tab2, tbAr21, tbAr22, tbAr23);
	tbArComp(tbAr11, tbAr21, ok, clear);
	tbArComp(tbAr12, tbAr22, numOk, clear);
	tbArComp(tbAr13, tbAr23, numCombOk, clear);
	int tot = max(tbAr11.size(), tbAr21.size());
	/*
	cout << "Comparison ended successfully\n";
	cout << "File 1: " << seg1 << " bars\n";
	cout << "File 2: " << seg2 << " bars\n";
	*/
	cout << numOkSeg << " " << min(seg1, seg2) << '\n';
	cout << numOk << " " << tot << " " << clear << "\n";
	cout << numCombOk << " " << tot << " " << clear << "\n";

	return 0;
}
