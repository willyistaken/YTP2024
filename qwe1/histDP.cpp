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

	// vector<int> www;
	// for (int i = 0; i < (int)W.size(); ++i)
	//	for (int j = 0; j < (int)W[j].size(); ++j)
	//		if (W[i][j] > 0)
	//			www.emplace_back(W[i][j]);
	// sort(www.begin(), www.end());
	// int thres = www[(int)size(www) / 2];
	int thres = 0;

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

	vector<vector<array<int, 3>>> dp((int)events.size()); // val, fromId1, fromId2
	array<int, 3> tmp;
	if (!mp.count(events[0]))
		dp[0].emplace_back(tmp = {0, -1, -1});
	else {
		for (int i = 0; i < (int)mp[events[0]].size(); ++i)
			dp[0].emplace_back(tmp = {0, -1, -1});
	}

	const int mxDif = 4;

	int lst = 0;
	for (int i = 1; i < (int)events.size(); ++i) {
		if (events[i].empty()) continue;
		if (!mp.count(events[i])) {
			int id = 0;
			for (int j = 1; j < (int)dp[lst].size(); ++j)
				if (dp[lst][j][0] > dp[lst][id][0])
					id = j;
			dp[i].emplace_back(tmp = {dp[lst][id][0], lst, id});
			lst = i;
			continue;
		}

		if (!mp.count(events[lst]) || i - lst > mxDif) {
			int id = 0;
			for (int j = 1; j < (int)dp[lst].size(); ++j)
				if (dp[lst][j][0] > dp[lst][id][0])
					id = j;
			for (int j = 0; j < (int)mp[events[i]].size(); ++j)
				dp[i].emplace_back(tmp = {dp[lst][id][0], lst, id});
			lst = i;
			continue;
		}

		for (int j = 0; j < (int)mp[events[i]].size(); ++j) {
			tmp = {-1, -1, -1};
			for (int k = 0; k < (int)dp[lst].size(); ++k) {
				int val = dp[lst][k][0] + (W[mp[events[lst]][k]][mp[events[i]][j]] > thres);
				if (tmp[0] < val)
					tmp = {val, lst, k};
			}
			dp[i].emplace_back(tmp);
		}
		lst = i;
	}

	vector<vector<int>> tab((int)V[0].size(), vector<int>((int)events.size(), -1));
	int id2 = 0;
	for (int i = 1; i < (int)dp[lst].size(); ++i)
		if (dp[lst][i] > dp[lst][id2])
			id2 = i;
	while (lst != -1) {
		if (mp.count(events[lst])) {
			for (int i = 0; i < (int)tab.size(); ++i)
				tab[i][lst] = V[mp[events[lst]][id2]][i];
		}
		int _l = lst, _i = id2;
		lst = dp[_l][_i][1];
		id2 = dp[_l][_i][2];
	}

	cout << (int)tab.size() << '\n' << (int)tab[0].size() << '\n';
	for (auto &i : tab) {
		for (auto &j : i)
			cout << j << ' ';
		cout << '\n';
	}

	return 0;
}
