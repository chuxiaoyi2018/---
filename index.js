//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    motto: '检测结果：',
    value: '0',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    userVideo: "",
    img_arr: [],
  },
  //事件处理函数
  onShareAppMessage: function () {
    return {
      title: 'OCRDemo小程序',
      path: '/pages/ocr/ocr',
      success: function (res) {
        if (res.errMsg == 'shareAppMessage:ok') {
          wx.showToast({
            title: '分享成功',
            icon: 'success',
            duration: 500
          });
        }
      },
      fail: function (res) {
        if (res.errMsg == 'shareAppMessage:fail cancel') {
          wx.showToast({
            title: '分享取消',
            icon: 'loading',
            duration: 500
          })
        }
      }
    }
  },
  clear: function (event) {
    console.info(event);
    wx.clearStorage();
  },
  //事件处理函数
  bindViewTap: function () {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },


  videoSelect: function () {
    var that = this //！！！！！！！！！“搭桥”
    //利用API从本地读取一张图片
    wx.chooseVideo({
      sourceType: ['album', 'camera'],
      success: function (res) {
        var tempFilePath = res.tempFilePath
        //将读取的图片替换之前的图片
        that.setData(
          {
            userVideo: tempFilePath,
            img_arr: that.data.img_arr.concat(tempFilePath),
          }
        )//通过that访问
        console.log(that.data.userVideo)
      }
    })
  },
  changeName: function (e) {
    this.setData({
      value: "xiao",
    })

  },
  upload: function () {
    var that = this
    wx.uploadFile({
      url: 'http://127.0.0.1:8090/postdata',
      // filePath: that.data.img_arr[0],
      filePath: that.data.userVideo,
      name: 'content',
      header: {
        "content-type": "multipart/form-data"
      },
      // formData: adds,
      success: function (res) {
        console.log(res.data);



        if (res) {
          wx.showToast({
            title: 'gif生成成功！！',
            duration: 10000
          });
          wx.previewImage({
            current: 'D:/search/py_workplace/new.gif',
            urls: ["D:/research/py_workplace/new.gif"],
          })
        }
      }
    })
    this.setData({
      formdata: ''
    })
  },
  onLoad: function () {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse) {
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
  },
  getUserInfo: function (e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  }



})
