var app = new Vue({
  el: '#app',
  data: {
    message: 'Hello Vue!',
    scale:1280/814,
    pen_is_finished:false,
    videoController: 'Pause',
    videoControllerClass:["ui","orange","button"],
    penStatus:false,
    bboxes:[],
    bboxes0:[],
    bboxes_length:0,
    bboxes0_length:0,
    board:{},
    modalClass:["ui","modal"],
    imgDataURL:"",
    inputID:null,
    changingBboxesPos:0,
    renderBboxes:[],
    renderBboxes0:[],
    trackbar:{
      pos:0,
      stat:false,
      len:1,
      width:0,
      left:0
    },
    renderbar:null,
    picked:[],
  },
  methods: {
    videoControll:function(){

      if(this.videoController == "Pause"){
        // pause the video
        this.$refs.video.pause();
        this.videoController = "Play";
        this.videoControllerClass[1] = "green";
      }
      else{
        // play the video
        this.$refs.video.play();
        this.bboxes = [];
        this.bboxes_length = 0;
        this.videoController = "Pause";
        this.videoControllerClass[1] = "orange";
      }

    },
    penDown:function(event){
      // console.log(this.$refs.board.offsetLeft);
      if(this.videoController == "Play"){
        console.log("Pen Down.");
        // console.log(this.board.x);
        this.penStatus = true;
        var _color = "hsla("+parseInt(Math.random()*360)+", 100%, 78%, 0.78)";
        var _bbox = {
          id:"ID-"+this.bboxes0_length,
          data:{
            x0:event.pageX - this.board.x,
            y0:event.pageY - this.board.y,
            x1:event.pageX - this.board.x,
            y1:event.pageY - this.board.y,
          },
          style:{
            left:(event.pageX - this.board.x) + "px",
            top:(event.pageY - this.board.y) + "px",
            width:0,
            height:0,
            borderColor:_color
          },
          infoStyle:{
            left:(event.pageX - this.board.x) + "px",
            top:(event.pageY - this.board.y) + "px",
            width:0,
            // height:0,
            backgroundColor:_color,
            display:"none"
          }
        };

        this.bboxes.push(_bbox);
        this.bboxes0.push(_bbox);
        this.bboxes_length ++;
        this.bboxes0_length ++;
      }

    },
    penMove:function(event){
      if(this.penStatus == true){
        event.preventDefault();
        this.bboxes[this.bboxes_length-1].style.width =  (event.pageX - this.board.x - this.bboxes[this.bboxes_length-1].data.x0) + "px";
        this.bboxes[this.bboxes_length-1].style.height = (event.pageY - this.board.y - this.bboxes[this.bboxes_length-1].data.y0) + "px";
        this.bboxes[this.bboxes_length-1].data.x1 = event.pageX - this.board.x;
        this.bboxes[this.bboxes_length-1].data.y1 = event.pageY - this.board.y;
      }

    },
    penUp:function(event){
      if(this.penStatus == true){
        this.bboxes[this.bboxes_length-1].style.width =  (event.pageX - this.board.x - this.bboxes[this.bboxes_length-1].data.x0) + "px";
        this.bboxes[this.bboxes_length-1].style.height = (event.pageY - this.board.y - this.bboxes[this.bboxes_length-1].data.y0) + "px";
        this.bboxes[this.bboxes_length-1].data.x1 = event.pageX - this.board.x;
        this.bboxes[this.bboxes_length-1].data.y1 = event.pageY - this.board.y;

        this.bboxes[this.bboxes_length-1].infoStyle.top = (this.bboxes[this.bboxes_length-1].data.y1 + 6) + "px";
        this.bboxes[this.bboxes_length-1].infoStyle.width = this.bboxes[this.bboxes_length-1].style.width;
        this.bboxes[this.bboxes_length-1].infoStyle.display = "inline-block";

        this.bboxes0[this.bboxes0_length-1] = this.bboxes[this.bboxes_length-1];
        // //can use bboxes0[pos] = bboxes[pos], but i am not sure the risk for now.
        // this.bboxes0[this.bboxes0_length-1].style.width =  (event.pageX - this.board.x - this.bboxes0[this.bboxes0_length-1].data.x0) + "px";
        // this.bboxes0[this.bboxes0_length-1].style.height = (event.pageY - this.board.y - this.bboxes0[this.bboxes0_length-1].data.y0) + "px";
        // this.bboxes0[this.bboxes0_length-1].data.x1 = event.pageX - this.board.x;
        // this.bboxes0[this.bboxes0_length-1].data.y1 = event.pageY - this.board.y;
        //
        // this.bboxes0[this.bboxes0_length-1].infoStyle.top = (this.bboxes0[this.bboxes0_length-1].data.y1 + 6) + "px";
        // this.bboxes0[this.bboxes0_length-1].infoStyle.width = this.bboxes0[this.bboxes0_length-1].style.width;
        // this.bboxes0[this.bboxes0_length-1].infoStyle.display = "inline-block";
        // xes[this.bboxes0_length-1].data.y1 + 3) ;
        this.penStatus = false;
        console.log("Pen up.");
      }
    },
    changeID:function(i,event){
      console.log("Start change ID.");
      this.changingBboxesPos = i;
      // this.modalClass.active = true;
      // this.modalClass.push("active");
      var bboxCanvas = document.createElement("canvas");
      bboxCanvas.width =  this.bboxes[i].data.x1-this.bboxes[i].data.x0;
      bboxCanvas.height =  this.bboxes[i].data.y1-this.bboxes[i].data.y0;
      var ctx = bboxCanvas.getContext("2d");
      // console.log( bboxs[i].x, bboxs[i].y, bboxs[i].width, bboxs[i].height, bboxs[i].width*scale,bboxs[i].height*scale);
      ctx.drawImage(this.$refs.video,
                    this.bboxes[i].data.x0*this.scale,
                    this.bboxes[i].data.y0*this.scale,
                    bboxCanvas.width*this.scale,
                    bboxCanvas.width*this.scale,

                    0,0,
                    bboxCanvas.width,bboxCanvas.width
                  );
      this.imgDataURL = bboxCanvas.toDataURL();
      // $("#tmp").append("<img src='"+bboxCanvas.toDataURL()+"'>");

      this.inputID = this.bboxes[i].id;
      $(".ui.modal").modal("show");
    },
    submitChange:function(){
      console.log("ID Changed successfully");
      this.bboxes[this.changingBboxesPos].id = this.inputID;
      console.log(this.bboxes[this.changingBboxesPos].id);
      $(".ui.modal").modal("hide");
    },
    updateTrackbar:function(event){
      // console.log(this.$refs.video.duration,this.trackbar.len,"+++");
      this.trackbar.pos = this.$refs.video.currentTime*100 / this.$refs.video.duration;
      $("#progressor").progress({percent: this.trackbar.pos});
    },
    trackbarDown:function(event){
      console.log("change the currentTime of video");
      this.trackbar.stat = true;

      this.trackbar.pos = 100*(event.pageX - this.trackbar.left) / this.trackbar.width;
      $("#progressor").progress({percent: this.trackbar.pos});
      this.$refs.video.currentTime = this.trackbar.pos * this.$refs.video.duration / 100;
    },
    trackbarMove:function(event){
      if(this.trackbar.stat == true){
        this.trackbar.pos = 100*(event.pageX - this.trackbar.left) / this.trackbar.width;
        $("#progressor").progress({percent: this.trackbar.pos});
        this.$refs.video.currentTime = this.trackbar.pos * this.$refs.video.duration / 100;
      }
    },
    trackbarUp:function(event){
      if(this.trackbar.stat == true){
        this.trackbar.pos = 100*(event.pageX - this.trackbar.left) / this.trackbar.width;
        $("#progressor").progress({percent: this.trackbar.pos});
        this.$refs.video.currentTime = this.trackbar.pos * this.$refs.video.duration / 100;
        this.trackbar.stat = false;
      }
    },
    renderVideo:function(){
      var self = this;
      $.ajax({
        url:"http://localhost:5000/render/trackbar",
        method:"POST",
        dataType:"json",
        data: JSON.stringify({
            find:self.picked
        }),
        success:function(resp){
          self.renderbar.renderData(resp.prob);
          self.renderBboxes0 = resp.bboxes;
          console.log("return rendered bboxes:",resp.bboxes);
          setInterval(function(){
            self.drawRenderBboxes();
          },125)
        }
      });

    },
    drawRenderBboxes:function(){
      // console.log("painting invertal.");
      var _currentTime = this.$refs.video.currentTime * 1000, b_len = this.renderBboxes0.length;
      this.renderBboxes = [];
      for(var i=0;i<b_len;i++){
        if(this.renderBboxes0[i].time* 1000 >= _currentTime - 120 && this.renderBboxes0[i].time* 1000 <= _currentTime + 120){
          this.renderBboxes.push(this.renderBboxes0[i]);
        }
      }
    },
    saveBboxes:function(){
      var self = this;
      $.ajax({
        url:"http://localhost:5000/api/bboxes",
        method:"POST",
        dataType:"json",
        data: JSON.stringify({
            bboxes:this.bboxes0
        }),
        success:function(resp){
          console.log("success!!!");
        }
      });
    }
  },
  created:function(){
  },
  mounted:function(){
    this.board.x = $("#frame").offset().left;

    this.board.y = $("#frame").offset().top;

    this.board.width = this.$refs.board.offsetWidth;
    // console.log("the board width is",this.board.width);
    this.board.height = this.$refs.board.offsetHeight;

    this.scale = 1280/this.board.width;

    // this.trackbar.len = this.$refs.video.duration;
    // cannot get duration here.
    this.trackbar.left = $("#progressor").offset().left;
    this.trackbar.width = $("#progressor").width();
    console.log(this.trackbar.len,this.$refs.video.duration);
    $("#progressor").progress({percent:0});
    // this.trackbar.len = this.$refs.video.duration;
    // this.trackbar.left = $("#progressor").offset().left;
    // this.trackbar.width = $("#progressor").width();
    // console.log(this.trackbar.len,this.$refs.video.duration);
    // $("#progressor").progress({percent:0});
    this.renderbar = new RenderBar(this.$refs.renderbar);

  },
  updated:function(){
    // this.trackbar.len = this.$refs.video.duration;
    // this.trackbar.left = $("#progressor").offset().left;
    // this.trackbar.width = $("#progressor").width();
    // console.log(this.trackbar.len,this.$refs.video.duration);
    // $("#progressor").progress({percent:0});
  }
  })
