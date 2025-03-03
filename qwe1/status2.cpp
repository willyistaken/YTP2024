#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <map>
#include <cassert>
#include <iomanip>
#include <numeric>
using namespace std;

const int base[] = {64, 59, 55, 50, 45, 40};

int main(int argc, char* argv[]) {
	if (argc < 2) {
		cerr << "Usage: " << argv[0] << " <hist file>\n";
		return 1;
	}
	
	string file1 = argv[1];
	ifstream inFile1(file1);
	if (!inFile1) {
		cerr << "Error: Could not open file " << file1 << '\n';
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

	//vector<int> www;
	//for (int i = 0; i < (int)W.size(); ++i)
	//	for (int j = 0; j < (int)W[j].size(); ++j)
	//		if (W[i][j] > 0)
	//			www.emplace_back(W[i][j]);
	//sort(www.begin(), www.end());
	//for (int i = 1; i < 200; ++i)
	//	cerr << www[(int)www.size() - i] << ' ';
	// int thres = www[(int)size(www) / 2];
	int thres = 2;

	map<vector<int>, pair<int, vector<int>>> mp;

	for (int i = 0; i < (int)combCnt.size(); ++i) {
		vector<int> c;
		for (int j = 0; j < (int)V[i].size(); ++j)
			if (V[i][j] != -1)
				c.emplace_back(base[j] + V[i][j]);
		sort(c.begin(), c.end());
		mp[c].second.emplace_back(combCnt[i]);
		mp[c].first += combCnt[i];
	}

	cout << (int)combCnt.size() << ' ' << (int)mp.size() << '\n'; // 2526 1836

	vector<pair<int, vector<int>>> vmp;
	for (auto &i : mp) {
		vmp.emplace_back(i.second);
		sort(vmp.back().second.begin(), vmp.back().second.end());
		reverse(vmp.back().second.begin(), vmp.back().second.end());
	}

	sort(vmp.begin(), vmp.end());
	reverse(vmp.begin(), vmp.end());
	while (vmp.back().first < 50)
		vmp.pop_back();

	vector<int> cnt(101, 0);

	for (auto [tot, vi] : vmp) {
		//cout << tot << ' ' << 1.0 * tot / sum << '\n';
		
		++cnt[100*vi[0]/tot];
	}
	for (int i = 99; i >= 0; --i)
		cnt[i] += cnt[i + 1];
	cout << fixed << setprecision(5);
	cout << cnt[0] << '\n';
	for (auto i = 0; i <= 100; ++i)
		cout << i << ' ' << cnt[i] << ' ' << 1.0 * cnt[i] / cnt[0] << '\n';
	cout << '\n';

	return 0;
}
