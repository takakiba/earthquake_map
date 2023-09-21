from libcomcat.search import search
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mplcolors
import os
import numpy as np
import cartopy.crs as ccrs
import tqdm 

import makemovie


if __name__ == '__main__':

    ### create directory to save png files
    file_path = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.basename(__file__)
    data_path = os.path.abspath(file_path + '/../data/' + file_name.split(".")[0] + '/')
    if not os.path.isdir(data_path): os.makedirs(data_path)


    ### retrieve the earthquake data
    time_events = search(
            starttime=datetime.datetime(2011, 1, 1, 0, 0), 
            endtime=datetime.datetime(2011, 12, 31, 23, 59),
            minmagnitude = 5.0
            )

    ### create dataframe of earthqueakes
    time_list = [e.time for e in time_events]
    mag_list  = [e.magnitude for e in time_events]
    lat_list  = [e.latitude for e in time_events]
    long_list = [e.longitude for e in time_events]
    dep_list  = [e.depth for e in time_events]

    df = pd.DataFrame({
        'Date time': time_list,
        'Magnitude': mag_list,
        'Latitude' : lat_list,
        'Longitude': long_list,
        'Depth'    : dep_list
        })

    ### count days of data collection
    days = (df.iloc[-1,:]['Date time'] - df.iloc[0,:]['Date time']).days

    ### make list of days for plot
    tmp_date = df.iloc[0,:]['Date time'].date()
    plot_date_list = [tmp_date]
    for i in range(days):
        tmp_date += datetime.timedelta(days=1)
        plot_date_list.append(tmp_date)


    ### prepara campus to plot
    fig = plt.figure(figsize=(12, 6), dpi=120)

    ### parameter for transparency animation, increase accelerate dimming of plot
    alpha_const = 1.0
    ### parameter for plot marker size depending on magnitude
    size_const = 1.0
    # print('Marker max. : {0}'.format(np.max(np.exp(size_const * df['Magnitude']))))
    # print('Marker min. : {0}'.format(np.min(np.exp(size_const * df['Magnitude']))))

    ### loop for plotting in each day
    print('Drawing plot')
    for date in tqdm.tqdm(plot_date_list):
        # print('Date : {0:%Y-%m-%d}'.format(date))

        ### prepare axis
        ax1 = plt.axes(projection=ccrs.PlateCarree(central_longitude=150))

        ### draw world map
        ax1.coastlines(resolution='50m')
        ax1.set_extent((-180, 180, -90, 90))

        ### extract data to plot
        plot_df = df[(df['Date time'] <= datetime.datetime.combine(date, datetime.time(23, 59, 59)))]
        n_data = len(plot_df)

        ### difference between current plot and past date
        days_passed = np.array([(date - d.date()).days for d in plot_df['Date time']])
        # print(days_passed)

        ### determine transparency depending on days passed and magnitude
        alpha = np.exp(- alpha_const * days_passed / plot_df['Magnitude'])
        ### line colors list
        lc = [mplcolors.ColorConverter().to_rgba('red', a) for a in alpha]

        ### plot eathquake data on the date
        ax1.scatter(
                plot_df['Longitude'], 
                plot_df['Latitude'], 
                s=np.exp(size_const * plot_df['Magnitude']), 
                facecolor='None', edgecolors=lc,
                transform=ccrs.PlateCarree()
            )

        ### set title
        fig.suptitle('{0:%Y-%m-%d}'.format(date))

        ### finalize the figure and save data
        plt.tight_layout()
        plt.savefig(data_path + '/Map_on_{0:%Y-%m-%d}.png'.format(date))
        plt.clf()

    ### make animation movie data from sequence of png 
    print('Making movie')
    makemovie.make_movie(data_path, video_name='EQ_movie')








