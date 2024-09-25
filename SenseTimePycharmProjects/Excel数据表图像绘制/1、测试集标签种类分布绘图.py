import os
import matplotlib.pyplot as plt
import pandas as pd

class PlotDataChart:

    def __init__(self,data_file_path,model_name):
        self.data_file_path = data_file_path
        self.model_name = model_name
        self.rear_excel_file()
        pass

    def plot_pie_chart(self,df):
        plt.figure(figsize=(8, 6))  # 设置图形大小
        plt.pie(df['valid(by_ins)'], labels=df['Unnamed: 0'], autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # 确保饼图是圆形
        plt.title('Category Distribution')  # 设置标题
        # plt.imsave("/data/had_test_datelist/had_images_sample_info_statistics/TSR/Pie_chart.png")
        plt.savefig('/data/had_test_datelist/had_images_sample_info_statistics/'+self.model_name+'/Test_Pie_chart.png',
                    dpi=300)  # dpi参数控制图像的分辨率
        # plt.show()

    def rear_excel_file(self):
        df = pd.read_excel(self.data_file_path)
        df = df.drop(0).iloc[:,0:2]
        print(df)
        self.plot_pie_chart(df)

        # 绘制饼状图

        pass

input_info = {
              "origin_file_path":r"/data/had_test_datelist/had_images_sample_info_statistics",
              "model_name_list":["TLR",'TSR',"animal","obstacle","pole","rear_roadmarker","roadmarker"],
              "excel_data_file_name":"test.xlsx"
              }

for model_name in input_info["model_name_list"]:
    excel_file_path = os.path.join(input_info["origin_file_path"],model_name,input_info["excel_data_file_name"])
    plot_chart = PlotDataChart(excel_file_path,model_name)



