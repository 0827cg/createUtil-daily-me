package com.cgtest.kmpsearch;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

/**
 * @author cg
 *	time: 2017-09-15
 *	describe: use kmp algorithm to search files by string
 */
public class KMPsearchFile {
	
	public static void main(String [] args) {
		
		System.out.println("ͨ���ַ����������ļ���ʹ��ȫƥ��Ļ��ڲ���ƥ����KMP�㷨");
		Scanner scanner = new Scanner(System.in);
		while(true){
			System.out.println("�������ļ�·��('q to exit') :");
			String strFilePath = scanner.nextLine();
			if(strFilePath.equals("q") || strFilePath.equals("Q")) {
				scanner.close();
				break;
			}else if(!strFilePath.equals("")){
				if(new File((strFilePath)).exists() && true) {
					System.out.println("������Ҫ���ҵ��ַ��� :");
					String strSearch = scanner.nextLine();
					if(strSearch.equals("q") || strSearch.equals("Q")) {
						scanner.close();
						break;
					}else {
						
						long startTime = System.currentTimeMillis();
						
						KMPself kmpself = new KMPself();
						int [] kmpTable = kmpself.getKMPtable(strSearch);
							
						Map<String, Object> mapTotalFile = kmpself.kmpSearchFileByStr(strFilePath, strSearch, kmpTable);
						double userTime = (System.currentTimeMillis() - startTime);
						kmpself.showResult(mapTotalFile);
						System.out.println("���Һ�ʱ:" + (userTime)/1000 + "s");
						}
						
					}
				}else {
					System.out.println("�ļ�·��" + strFilePath + "������");
					continue;
				}
			}
		}
		
}


class KMPself{
	
	ArrayList<File> listFilesObj = null;
	
	@SuppressWarnings("unchecked")
	public void showResult(Map<String, Object> mapTotalFile) {
		
		ArrayList<Object> listMsg = (ArrayList<Object>) mapTotalFile.get("resultMsg");
		System.out.println("<-----���ҽ��----->");
		System.out.println("����·��Ϊ:" + mapTotalFile.get("searchPath"));
		System.out.println("���ҵ��ַ���Ϊ:" + mapTotalFile.get("strSearch"));
		if(listMsg == null || listMsg.size() == 0) {
			System.out.println("��ɨ���ļ����� :" + mapTotalFile.get("fileNum"));
			System.out.println("��ɨ���ַ����� :" + mapTotalFile.get("totalCharNum"));
			System.out.println("��Ǹ , δ���ҵ���Ӧ�ļ�");
		}else {
			System.out.println("�������ַ������ļ�·������������ :");
			for(int i = 0; i < listMsg.size(); i++) {
				Map<String, Object> mapItem = (Map<String, Object>) listMsg.get(i);
				System.out.println("�ļ�" + (i + 1) + "·�� :" + mapItem.get("filePath"));
				System.out.println("���ָ��ַ��������� :" + mapItem.get("totalCount"));
				System.out.println("���ָ��ַ��������� :" + mapItem.get("lineNum"));
				System.out.println("������Ӧ�ĳ��ִ��� :" + mapItem.get("lineExistCount"));
			}
			System.out.println("�ܲ����ļ����� :" + mapTotalFile.get("fileNum"));
			System.out.println("�ܲ����ַ����� :" + mapTotalFile.get("totalCharNum"));
			System.out.println("<-----�������----->");
		}
	}
	
	
	public ArrayList<File> getFiles(String strFilePath) {
		
		if(listFilesObj == null) {
			listFilesObj = new ArrayList<File>();
		}

		File fileObj = new File(strFilePath);
		
		if(fileObj.isDirectory()) {
			File fileNextDir [] = fileObj.listFiles();
			for(File fileItem : fileNextDir) {
				if(fileItem.isDirectory()) {
					getFiles(fileItem.getPath());
				}else {
					listFilesObj.add(fileItem);
				}
			}
		}else {
			listFilesObj.add(fileObj);
		}
		return listFilesObj;
	}
	
	
	public Map<String, Object> kmpSearchFileByStr(String strFilePath, String strSearch, int kmpTable []) {
		
		/*
		 * ʹ��kmp�㷨
		 * ͨ���ַ��������ļ������������Ľ����װ��map��list��ϼ����У������շ���һ��map����
		 */
		
		ArrayList<File> listFilesObj = getFiles(strFilePath);
		
		Map<String, Object> mapTotalFile = new HashMap<String, Object>();
		ArrayList<Object> listMsg = new ArrayList<Object>();
		int fileNum = 0;
		long totalCharNum = 0;
		
		for(File listItem : listFilesObj) {
			Map<String, Object> mapFile = new HashMap<String, Object>();
			ArrayList<Integer> listLineNum = new ArrayList<Integer>();
			ArrayList<Integer> listLineExistCount = new ArrayList<Integer>();
			int lineNum = 1;
			int existCount = 0;
			int totalCount = 0;
			try {
				BufferedReader buffererReader = new BufferedReader(new FileReader(listItem));
				String strLine = null;
				while((strLine = buffererReader.readLine()) != null) {
					existCount = kmpSearchStrByStr(strLine, strSearch, kmpTable);
					if(existCount != 0) {
						listLineNum.add(lineNum);
						listLineExistCount.add(existCount);
					}
					totalCharNum += strLine.length();
					totalCount += existCount;
					
					lineNum++;
				}
				buffererReader.close();
				if(totalCount != 0) {
					mapFile.put("filePath", listItem);
					mapFile.put("totalCount", totalCount);
					mapFile.put("lineNum", listLineNum);
					mapFile.put("lineExistCount", listLineExistCount);
				}
				if( mapFile.size() != 0) {
					listMsg.add(mapFile);
				}
				
			} catch (FileNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			fileNum++;
		}
		if(listMsg.size() != 0) {
			mapTotalFile.put("resultMsg", listMsg);
		}
		mapTotalFile.put("searchPath", strFilePath);
		mapTotalFile.put("strSearch", strSearch);
		mapTotalFile.put("fileNum", fileNum);
		mapTotalFile.put("totalCharNum", totalCharNum);
		
		return mapTotalFile;
	}
	
	
	public int kmpSearchStrByStr(String totalStr, String strSearch, int kmpTable []) {
		/*
		 * ����1Ϊ�����ַ���
		 * ����2Ϊ����������ַ�����������
		 * ����3Ϊ����������ַ����Ĳ���ƥ����ֵ��Ϊint���͵�һά����
		 * ȫƥ��Ļ��ڲ���ƥ����KMP�㷨
		 * �����ǻ���next����
		 * 
		 * �䷵��ֵ�ǵ�ǰ�ַ������г����������ĸ���
		 * ��ʱ�����±�
		 * 
		 */
		char searchChar [] = strSearch.toCharArray();
		char totalChar [] = totalStr.toCharArray();
		
		int s = 0;
		int t = 0;
		//int index = -1;
		int existCount = 0;
		while(s < searchChar.length && t < totalChar.length) {
			if(searchChar[s] == totalChar[t]) {
				if((s + 1) != searchChar.length) {
					s++;
					t++;
				}else {
					existCount++;
					if((totalChar.length - (t + 1)) >= searchChar.length) {
						s = 0;
						t++;
					}else {
						break;
					}
				}
			}else if(s == 0){
				s = 0;
				t++;
			}else {
				s = s - (s - kmpTable[(s - 1)]);
			}
			if((t + 1) >= totalChar.length) {
				break;
			}
		}
		return existCount;
		
	}
	
	
	
	public int[] getKMPtable(String strInput) {
		
		/*
		 * ��ȡkmp�Ĳ���ƥ����ֵ��
		 * �����Ȼ�ȡ�ַ������п��ܳ��ȵ���󹫸�Ԫ�س��ȣ������ŵ�int�����з���
		 */
		
		int intTablesLength = strInput.length();
		int kmp_table [] = new int [intTablesLength];
		
		for(int i = 0; i < strInput.length(); i++) {
			String strItem = strInput.substring(0, i + 1);
			int intMaxPublicNum = getMaxPublicNum(strItem);
			kmp_table [i] = intMaxPublicNum;
		}
		return kmp_table;
		
	}
	
	
	public int getMaxPublicNum(String strItem) {
		
		//��ȡǰ׺�ͺ�׺�������նԱȵõ����Ĺ���Ԫ�س���,������
		
		int intMaxPublicNum = 0;
		int intItemLength = strItem.length();
		
		String strFront [] = new String [intItemLength - 1];
		String strBack [] = new String [intItemLength - 1];
		
		for(int i = 0; i < intItemLength - 1; i++) {
			strFront[i] = strItem.substring(0, i + 1);
		}
		for(int i = intItemLength; i > 1; i--) {
			strBack[intItemLength - i] = strItem.substring(i - 1, intItemLength);
		}
		
		int n = -1;
		for(int i = 0; i < intItemLength - 1; i++) {
			if(strFront[i].equals(strBack[i])) {
				n = i;
			}
		}
		if(n != -1) {
			intMaxPublicNum = strFront[n].length();
		}
		return intMaxPublicNum;
	}
	
	
}

