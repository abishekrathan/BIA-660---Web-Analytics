# Assignment 5
# Abishek Lakshmirathan
import bs4
import time
import datetime
import unicodedata
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
from dateutil.parser import parse
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import numpy as np
from scipy.spatial.distance import cdist, euclidean
import statistics
import matplotlib.pyplot as plt
from heapq import nsmallest


# Task 1
# Scrape data function


def scrape_data(start_date, from_place, to_place, city_name):
    driver = webdriver.Chrome()
    driver.get('https://www.google.com/flights/explore/')
    from_field = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[2]/div')
    from_field.click()
    actions = ActionChains(driver)
    actions.send_keys(from_place)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(1)
    to_field = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[4]/div/div')
    to_field.click()
    actions = ActionChains(driver)
    actions.send_keys(to_place)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(1)
    current_url = str(driver.current_url)

    url_as_a_list = current_url.split('d=')
    del (url_as_a_list[1])
    url_as_a_list.append('d=' + start_date)
    url = ''.join(url_as_a_list)
    driver.get(url)
    time.sleep(3)
    city_results = driver.find_elements_by_class_name('LJTSM3-v-c')
    count = -1
    for item in city_results:
        count += 1
        if city_name.lower() in ''.join((c for c in unicodedata.normalize('NFD', item.text) if
                                         unicodedata.category(c) != 'Mn')).upper().lower():
            index = count

    results = driver.find_elements_by_class_name('LJTSM3-v-d')
    test = results[index]
    bars = test.find_elements_by_class_name('LJTSM3-w-x')
    data = []

    for bar in bars:
        ActionChains(driver).move_to_element(bar).perform()
        time.sleep(0.001)
        data.append((test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text,
                     test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text))
    # clean_data = [(float(d[0].replace('$', '').replace(',', '')), (parse(d[1].split('-')[0].strip()))) for d in
    #               data]
    # df = pd.DataFrame(clean_data, columns=['Price', 'Start_Date'])
    df = clean_data(data)
    return df

def scrape_data_90(start_date, from_place, to_place, city_name):
    driver = webdriver.Chrome()
    driver.get('https://www.google.com/flights/explore/')
    from_field = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[2]/div')
    from_field.click()
    actions = ActionChains(driver)
    actions.send_keys(from_place)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(1)
    to_field = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[4]/div/div')
    to_field.click()
    actions = ActionChains(driver)
    actions.send_keys(to_place)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(1)
    current_url = str(driver.current_url)

    url_as_a_list = current_url.split('d=')
    del (url_as_a_list[1])
    url_as_a_list.append('d=' + start_date)
    url = ''.join(url_as_a_list)
    driver.get(url)
    time.sleep(3)
    city_results = driver.find_elements_by_class_name('LJTSM3-v-c')
    count = -1
    for item in city_results:
        count += 1
        if city_name.lower() in ''.join((c for c in unicodedata.normalize('NFD', item.text) if
                                         unicodedata.category(c) != 'Mn')).upper().lower():
            index = count

    results = driver.find_elements_by_class_name('LJTSM3-v-d')
    test = results[index]
    next_btn = driver.find_element_by_class_name('LJTSM3-w-D')
    bars = test.find_elements_by_class_name('LJTSM3-w-x')
    data = []

    for bar in bars:
        ActionChains(driver).move_to_element(bar).perform()
        time.sleep(0.001)
        data.append((test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text,
                     test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text))
    time.sleep(2)
    ActionChains(driver).move_to_element(next_btn).perform()
    time.sleep(2)
    next_btn.click()
    time.sleep(2)
    temp_count = -1

    temp_city_results = driver.find_elements_by_class_name('LJTSM3-v-c')
    for i in temp_city_results:
        temp_count = temp_count + 1
        if city_name.lower() in ''.join(
                (c for c in unicodedata.normalize('NFD', i.text) if unicodedata.category(c) != 'Mn')).upper().lower():
            new_index = temp_count

    results = driver.find_elements_by_class_name('LJTSM3-v-d')
    test = results[new_index]
    bars = test.find_elements_by_class_name('LJTSM3-w-x')
    for i in range(0, 30):
        ActionChains(driver).move_to_element(bars[i]).perform()
        time.sleep(0.001)
        data.append((test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text,
                     test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text))

    # clean_data = [(float(d[0].replace('$', '').replace(',', '')), (parse(d[1].split('-')[0].strip()))) for d in
    #               data]
    # df = pd.DataFrame(clean_data, columns=['Price', 'Start_Date'])

    df = clean_data(data)
    return df

def task_3_IQR(flight_data):
    flight_data.sort_values('Price', inplace=True)

    Q1 = flight_data['Price'].quantile(0.25)
    Q3 = flight_data['Price'].quantile(0.75)
    IQR = Q3 - Q1

    # Values between Q1-1.5IQR and Q3+1.5IQR
    filtered = flight_data.query('(@Q1 - 1.5 * @IQR) <= Price <= (@Q3 + 1.5 * @IQR)')
    fig = flight_data['Price'].plot.box()
    plt.savefig("task_3_iqr.png")
    return filtered.head()

def task_3_dbscan(flight_data):
    df_days = clean_data_days(flight_data)
    X = StandardScaler().fit_transform(df_days[['Start_Date', 'Price']])
    db = DBSCAN(eps=0.5, min_samples=3).fit(X)

    labels = db.labels_
    clusters = len(set(labels))
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    df_days['dbscan_labels'] = db.labels_

    outliers = (df_days['dbscan_labels'] == -1)
    plt.subplots(figsize=(12, 8))

    for k, c in zip(unique_labels, colors):
        class_member_mask = (labels == k)
        xy = X[class_member_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=c,
                 markeredgecolor='k', markersize=14)

    plt.title("Total Clusters: {}".format(clusters), fontsize=14,
              y=1.01)
    plt.savefig("task_3_dbscan.png")

    # get index list of outliers
    index_list_of_outliers = []
    for i, val in enumerate(outliers):
        if val == True:
            index_list_of_outliers.append(i)
    print index_list_of_outliers

    # get the distances to each clusters
    labels = db.labels_
    lbls = np.unique(db.labels_)
    print "Cluster labels: {}".format(np.unique(lbls))

    cluster_means = [np.mean(X[labels == num, :], axis=0) for num in range(lbls[-1] + 1)]
    print "Cluster Means: {}".format(cluster_means)
    # getting list of noise points
    noise_point_list = []
    for index in index_list_of_outliers:
        noise_point_list.append(X[index, :])
    print "Noise Points: {}".format(noise_point_list)

    # getting euclidean distance between noise point and each cluster mean
    dist = []
    list_of_dist = []
    for key, noise_point in enumerate(noise_point_list):
        for cm in cluster_means:
            dist.append(euclidean(noise_point, cm))

        list_of_dist.insert(key, dist)
        dist = []
    print "Euclidean distance: {}".format(list_of_dist)
    cluster_prices = []
    nearest_cluster_prices = []
    df_best_price = pd.DataFrame(columns=('Price', 'Start_Date'))
    for dis in list_of_dist:

        nearest_cluster_index = dis.index(min(dis))
        print nearest_cluster_index

        for key, x in enumerate(df_days['dbscan_labels']):
            if x == nearest_cluster_index:
                cluster_prices.append(df_days.iloc[key]['Price'])
        nearest_cluster_prices.append(cluster_prices)
        cluster_prices = []

    print nearest_cluster_prices
    # finding mean price of nearest cluster

    mean = []
    for price in nearest_cluster_prices:
        mean.append(sum(price) / len(price))

    std = []
    for price in nearest_cluster_prices:
        std.append(statistics.stdev(price))

    # finding list of outlier prices
    outlier_prices = []
    for val in index_list_of_outliers:
        outlier_prices.append(df_days.iloc[val]['Price'])
    print "Outlier prices: {}".format(outlier_prices)
    # finding best price
    df_best_price = pd.DataFrame(columns=('Start_Date', 'Price'))
    best_price_count = 0
    for x in range(0, (len(index_list_of_outliers)) - 1):

        m = int(mean[x])
        s = int(std[x])
        if (outlier_prices[x] < (m - (2 * s))) and (outlier_prices[x] < (m - 50)):
            best_price_count += 1
            df_best_price.loc[best_price_count] = flight_data.ix[index_list_of_outliers[x]]
    return df_best_price


def clean_data(data):
    clean_data = [(parse(d[1].split('-')[0].strip()), float(d[0].replace('$', '').replace(',', '')))
                  for d in data]
    df = pd.DataFrame(clean_data, columns=['Start_Date', 'Price'])

    return df


def clean_data_days(flight_data):
    df_day = pd.DataFrame(columns=['Start_Date', 'Price'])
    df_day['Price'] = flight_data['Price']
    days = []
    for i, x in enumerate(flight_data['Start_Date']):
        days.append(i)

    df_day['Start_Date'] = days

    return df_day

def task_4_dbscan(flight_data):
    df_days = clean_data_days(flight_data)
    
    X = StandardScaler().fit_transform(df_days[['Start_Date', 'Price']])
    db = DBSCAN(eps=.4, min_samples=5).fit(X)

    labels = db.labels_
    clusters = len(set(labels))
    unique_labels = set(labels)
    print unique_labels
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    index_list_of_clusters = []
    plt.subplots(figsize=(12, 8))
    list_of_coordinates = []
    for k, c in zip(unique_labels, colors):
        class_member_mask = (labels == k)
        xy = X[class_member_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=c,
                 markeredgecolor='k', markersize=14)
    plt.title("Total Clusters: {}".format(clusters), fontsize=14, y=1.01)
    plt.savefig("task_4_dbscan.png")
    df_days['dbscan_labels'] = db.labels_
    clstrs = [(df_days['dbscan_labels'] == i) for i in xrange(clusters)]
    outliers = (df_days['dbscan_labels'] == -1)
    # print len(outliers)
    # finding cluster wise index list
    for j, clstr in enumerate(clstrs):
        index_of_clusters = []
        if j != (len(clstrs) - 1):
            for i, value in enumerate(clstr):
                if value == True:
                    index_of_clusters.append(i)
            index_list_of_clusters.append(index_of_clusters)
    print index_list_of_clusters
    price = df_days['Price']
    # cluster wise price
    cluster_price_list = []
    cluster_price = []
    for value in index_list_of_clusters:
        for index in value:
            cluster_price.append(price[index])
        cluster_price_list.append(cluster_price)
        cluster_price = []

    print cluster_price_list

    # finding best price period

    flag_index = 0
    flag_average_price = 100000

    best_cluster = nsmallest(1, cluster_price_list)
    best_cluster_index = cluster_price_list.index(min(cluster_price_list))
    print best_cluster_index
    for i in range(0, len(best_cluster)):
        if i == len(best_cluster) - 5:
            break
        if len(best_cluster) > 5:
            maxi = max(best_cluster[i:i + 5])
            mini = min(best_cluster[i:i + 5])
            # print maxi,mini
            if maxi - mini < 20:
                temp_average = statistics.mean(best_cluster[i:i + 5])
                if temp_average < flag_average_price:
                    temp_best_period = best_cluster[i:i + 5]
                    flag_index = i
        elif len(best_cluster) == 5:
            # if len(item) == 5:
            maxi = max(best_cluster[i:i + 5])
            mini = min(best_cluster[i:i + 5])
            if maxi - mini < 20:
                temp_best_period = best_cluster[i:i + 5]
                flag_index = i
    # print temp_best_period


    df_best_period = pd.DataFrame(columns=('Start_Date', 'Price'))
    best_price_count = 0
    best_period_indices = index_list_of_clusters[best_cluster_index][flag_index:flag_index + 5]
    print "Best Price Indices:{}".format(best_period_indices)
    print "Best Price Period"
    for value in best_period_indices:
        df_best_period.loc[best_price_count] = flight_data.ix[value]
        best_price_count += 1
    return df_best_period


#print scrape_data('2017-04-18', 'New York', 'Scandinavia', 'alesund')

flight_data = scrape_data_90('2017-04-18', 'New York', 'Spain', 'malaga')
#print flight_data

#print task_3_dbscan(flight_data)

#print task_3_IQR(flight_data)

print task_4_dbscan(flight_data)
