#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <map>
#include <cassert>
using namespace std;

const int base[] = {64, 59, 55, 50, 45, 40};

int main(int argc, char* argv[]) {
	if (argc < 3) {
		cerr << "Usage: " << argv[0] << " <hist file> <note file>\n";
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

	int n;
	inFile1 >> n;
	vector<int> combCnt(n);
	for (int &i : combCnt)
		inFile1 >> i;
	inFile1 >> n;
	vector<vector<int>> V((int)combCnt.size(), vector<int>(n));
	for (auto &i : V) {
		for (int &j : i)
			inFile1 >> j;
	}

	vector<vector<int>> W((int)combCnt.size(), vector<int>((int)combCnt.size(), 0));
	for (int i = 0; i < (int)combCnt.size(); ++i) {
		inFile1 >> n;
		for (int x; n > 0; --n) {
			inFile1 >> x;
			++W[i][x];
		}
	}

	inFile2 >> n;
	vector<pair<int, int>> notes(n);
	for (auto &[a, b] : notes)
		inFile2 >> a >> b;

	vector<vector<int>> events(notes.back().second + 1, vector<int>(0));
	for (auto &[a, b] : notes)
		events[b].emplace_back(a);
	for (auto &i : events)
		sort(i.begin(), i.end());

	map<vector<int>, vector<int>> mp;

	for (int i = 0; i < (int)combCnt.size(); ++i) {
		vector<int> c;
		for (int j = 0; j < (int)V[i].size(); ++j)
			if (V[i][j] != -1)
				c.emplace_back(base[j] + V[i][j]);
		sort(c.begin(), c.end());
		mp[c].emplace_back(i);
	}

	vector<vector<int>> tab((int)V[0].size(), vector<int>((int)events.size(), -1));
	for (int i = 0, lst = -1; i < (int)events.size(); ++i) {
		if (events[i].empty()) continue;
		// assert(mp.count(events[i]));
		if (!mp.count(events[i])) {
			lst = -1;
			continue;
		}
		int b = -1;
		if (lst != -1) {
			int a = 0;
			for (int j : mp[events[i]])
				if (W[lst][j] > a)
					a = W[lst][j], b = j;
		}
		if (b == -1) {
			int a = 0;
			for (int j : mp[events[i]])
				if (combCnt[j] > a)
					a = combCnt[j], b = j;
		}
		for (int j = 0; j < (int)V[b].size(); ++j)
			tab[j][i] = V[b][j];
		lst = b;
	}

	cout << (int)tab.size() << '\n' << (int)tab[0].size() << '\n';
	for (auto &i : tab) {
		for (auto &j : i)
			cout << j << ' ';
		cout << '\n';
	}

	return 0;
}
