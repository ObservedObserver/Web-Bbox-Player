var RenderBar = function(dom){
  var self = this;
  this._init = function(dom){
    self.data = [];
    self.option = {
          grid: {
              left: '1%',
              right: '1%',
              bottom: '1%',
              top:'1%'
          },
          xAxis : [
              {
                  type : 'value',
                  show: false,
                  splitLine:{show:false},
              }
          ],
          yAxis : [
              {
                  type : 'value',
                  show: false,
                  splitLine:{show:false}
              }
          ],
          series : [
              {
                  type:'line',
                  symbol:'none',
                  areaStyle: {
                    smooth:true,
                    normal: {
                      color:'hsla(0, 100%, 65%, 0.48)'
                    }
                  },
                  data:this.data,
                  itemStyle : {
                    normal : {
                      lineStyle:{
                          color:'hsla(0, 100%, 65%, 0.78)'
                      }
                    }
                  },
              }
          ]
        };
    self.myChart = echarts.init(dom);
    self.myChart.setOption(self.option);
  };
  this.renderData = function(data){
    self.data = data;
    self.option.series = [];
    for(var i=0;i<data.length;i++){
      var _color = parseInt(Math.random()*360);
      var sub_series = {
          type:'line',
          symbol:'none',
          areaStyle: {
            smooth:true,
            normal: {
              color:'hsla('+_color+', 100%, 65%, 0.48)'
            }
          },
          data:data[i],
          itemStyle : {
            normal : {
              lineStyle:{
                  color:'hsla('+_color+', 100%, 65%, 0.78)'
              }
            }
          },
      };
      self.option.series.push(sub_series);
    }
    self.myChart.setOption(self.option);
  }
  this._init(dom);
}
