#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <filesystem>
#include <map>
using namespace std;
using namespace filesystem;

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

const int base[] = {63, 58, 54, 49, 44, 39};

map<vector<int>, int> id;
vector<int> combCnt;
vector<vector<int>> V;
vector<vector<int>> G;

const int mxDif = 4;

void tabCalc(vector<string> &tb) {
	if ((int)tb.size() != 7)
		return;
	for (int i = 2, cnt, lst = -1, dif = 0; i < (int)tb[0].size(); i += cnt) {
		cnt = tb.back()[i] - '0';
		if (tb[0][i] == '|')
			continue;
		vector<int> c;
		for (int j = 0; j < (int)tb.size() - 1; ++j) {
			string s;
			for (int k = 0; k < cnt; ++k)
				s += tb[j][i + k];
			while (!s.empty() && ('0' > s.back() || s.back() > '9'))
				s.pop_back();
			reverse(s.begin(), s.end());
			while (!s.empty() && ('0' > s.back() || s.back() > '9'))
				s.pop_back();
			reverse(s.begin(), s.end());
			if (s.empty()) c.emplace_back(-1);
			else c.emplace_back(stoi(s));
		}
		if (*max_element(c.begin(), c.end()) == -1) {
			++dif;
			continue;
		}
		if (!id.count(c)) {
			id[c] = (int)combCnt.size();
			combCnt.emplace_back(0), V.emplace_back(c);
			G.emplace_back(vector<int>(0));
		}
		++combCnt[id[c]];
		if (lst != -1 && dif <= mxDif)
			G[lst].emplace_back(id[c]);
		lst = id[c], dif = 0;
	}
}

int main(int argc, char* argv[]) {
	if (argc < 2) {
		cerr << "Usage: " << argv[0] << " <directory>\n";
		return 1;
	}

	path dir = argv[1];
	if (!exists(dir) || !is_directory(dir)) {
		cerr << "Error: Invalid folder path: " << dir << '\n';
		return 1;
	}

	for (const auto &entry : recursive_directory_iterator(dir)) {
		if (entry.is_regular_file() && entry.path().extension() == ".txt") {
			ifstream inFile(entry.path());
			vector<string> tab;
			if (handleFile(inFile, tab))
				tabCalc(tab);
		}
	}

	cout << (int)combCnt.size() << '\n';
	for (int i : combCnt)
		cout << i << ' ';
	cout << '\n';
	cout << (int)V[0].size() << '\n';
	for (auto &i : V) {
		for (auto &j : i)
			cout << j << ' ';
		cout << '\n';
	}
	for (auto &i : G) {
		cout << (int)i.size() << ' ';
		for (auto &j : i)
			cout << j << ' ';
		cout << '\n';
	}

	return 0;
}
