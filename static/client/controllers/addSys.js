controllers.controller("addSys", ["$scope","loading","$modalInstance","msgModal","sysService","errorModal",function ( $scope,loading,$modalInstance,msgModal,sysService,errorModal) {
    $scope.title = "新建巡检模板";
    $scope.args = {
        biz: "",
        template: "",
        script:"",
        max_num:"",
        comment:"",
        biz_l: []
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

    $scope.dbOption1 = {
        data: "bizList",
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
        sysService.add_sys({}, $scope.args, function (res) {
            loading.close();
            if (res.result) {
                msgModal.open("success", "添加模板成功！！");
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