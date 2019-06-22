controllers.controller("addTask", ["$scope","loading","$modalInstance","msgModal","sysService","errorModal",function ( $scope,loading,$modalInstance,msgModal,sysService,errorModal) {
    $scope.title = "新增任务";
    $scope.args = {
        biz: "",
        template: "",
        biz_l: [],
        host: '',
        task_name: '',
        task_type: '',
        time:'',
        late_time:''
    };
    // 查询业务
    $scope.bizList = [];
    $scope.inits = function () {
        loading.open();
        sysService.search_biz({}, {}, function (res) {
            loading.close();
            $scope.bizList = res.data;
            $scope.args.biz_l = res.data
        })
    };
    $scope.inits();


    // $scope.my_cli = function(){
    //
    //     laydate.render({
    //         elem:'#daterangepicker_demo2'
    //     })
    //
    //     alert($('#daterangepicker_demo2').val())
    // }
    //
    //
    // $('#daterangepicker_demo2').daterangepicker({
    //
    //     "timePicker": true,
    //     "timePicker24Hour": true,
    //     "linkedCalendars": false,
    //     "autoUpdateInput": false,
    //     "locale": {
    //         format: 'YYYY-MM-DD HH:mm:ss',
    //         separator: ' ~ ',
    //         applyLabel: "应用",
    //         cancelLabel: "取消",
    //         resetLabel: "重置",
    //     }
    // }, function (start, end, lable) {
    //     beginTimeStore = start;
    //     endTimeStore = end;
    //     alert(this.startDate.format(this.locale.format));
    //     alert(this.endDate.format(this.locale.format));
    //
    //
    // });

    $scope.hostList = [];
    $scope.search_host = function(){
        sysService.search_host({}, {biz_id: $scope.args.biz}, function (res) {
            loading.close();
            $scope.hostList = res.data
        });
    }

    // 查询所属业务的模板
    $scope.temList = [];
    $scope.select_biz = function(){
        loading.open();
        sysService.search_template({}, $scope.args, function (res) {

            $scope.temList = res.data
        });

       $scope.search_host();

    };

    $scope.dbOption2 = {
        data: "temList",
        multiple: false,
        modelData: ""
    };

    $scope.dbOption1 = {
        data: "bizList",
        multiple: false,
        modelData: ""
    };

    $scope.dbOption3 = {
        data: "hostList",
        multiple: false,
        modelData: ""
    };



    $scope.confirm = function () {
        if ($scope.args.biz == '') {
            msgModal.open("error", "请输入业务名！");
            return
        }
        if ($scope.args.template == '') {
            msgModal.open("error", "请输入模板名！");
            return
        }


        //请求后台函数存入数据
        loading.open();
        sysService.add_task({}, $scope.args, function (res) {
            loading.close();
            if (res.result) {
                msgModal.open("success", "添加任务成功！！");
                $modalInstance.close(res.data);
             }
            else {
                errorModal.open(res.msg);
             }
         })
    };

    $scope.cancel = function () {
        $modalInstance.dismiss("cancel");
    };


}]);