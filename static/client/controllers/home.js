controllers.controller("home", ["$scope", "loading", "$modal", "confirmModal", "sysService", "errorModal", "msgModal", function ($scope, loading, $modal, confirmModal, sysService, errorModal, msgModal) {

    $scope.args = {
        task_name: "",
        task_type: "",
    };

    //内容显示页数和数量
    $scope.PagingData = [];
    $scope.totalSerItems = 0;

    $scope.pagingOptions = {
        pageSizes: [10, 50, 100],
        pageSize: "10",
        currentPage: 1
    };
    $scope.template = [{id:1,text:"aaa"},{id:2,text:"bbb"}];

    $scope.templateOption = {
        data: "template",
        multiple: false,
    };


    $scope.inits = function () {
        loading.open();
        sysService.search_init({}, $scope.args, function (res) {
            loading.close();

        })
    };

    $scope.setPagingData = function (data, pageSize, page) {
        $scope.PagingData = data.slice((page - 1) * pageSize, page * pageSize);
        $scope.totalSerItems = data.length;
        if (!$scope.$$phase) {
            $scope.$apply();
        }
    };

    $scope.getPagedDataAsync = function (pageSize, page) {
        $scope.setPagingData($scope.hostList ? $scope.hostList : [], pageSize, page);
    };

    //查询系统表
    $scope.search_sys_info = function () {
        loading.open();
        sysService.search_task_info({}, $scope.args, function (res) {
            loading.close();
            if (res.result) {
                $scope.hostList = res.data;
                $scope.pagingOptions.currentPage = 1;
                $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
            } else {
                errorModal.open(res.msg);
            }
        })
    };
    $scope.search_sys_info();


    $scope.$watch('pagingOptions', function (newVal, oldVal) {
        $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
    }, true);


    $scope.exute_script = function(res){
        sysService.exute_script({}, res, function (res) {
            if (res.result) {

            } else {
                errorModal.open(res.msg);
            }
        })
    }


    $scope.add_sys = function () {
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/addtask.html',
            windowClass: 'dialog_custom',
            controller: 'addTask',
            backdrop: 'static'
        });
        modalInstance.result.then(function (res) {
            $scope.hostList.unshift(res);
            $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
            $scope.exute_script(res)
        })
    };

    $scope.modify_sys = function (row) {
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/addsys.html',
            windowClass: 'dialog_custom',
            controller: 'modifySys',
            backdrop: 'static',
            resolve: {
                objectItem: function () {
                    return row.entity;
                }
            }
        });
        modalInstance.result.then(function (res) {
            row.entity.sys_name = res.sys_name;
            row.entity.sys_code = res.sys_code;
            row.entity.owners = res.owners;
            row.entity.first_owner = res.first_owner;
            row.entity.is_control = res.is_control;
        })
    };


    $scope.delete_sys = function (row) {
        //根据id删除系统
        var id = row.entity.id;
        confirmModal.open({
            text: "确定删除该系统吗？",
            confirmClick: function () {
                loading.open();
                sysService.delete_sys({id: id}, {}, function (res) {
                    loading.close();
                    if (res.result) {
                        $scope.hostList.splice(row.rowIndex, 1);
                        msgModal.open("success", "删除系统成功！");
                        $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
                    }
                    else {
                        errorModal.open(res.message);
                    }
                })
            }
        });

    };


    $scope.gridOption = {
        data: "PagingData",
        enablePaging: true,
        enableColumnResize: true,
        showFooter: true,
        pagingOptions: $scope.pagingOptions,
        totalServerItems: 'totalSerItems',
        columnDefs: [
            {field: "task_name", displayName: "任务名称", width: 200},
            {field: "host", displayName: "巡检服务器", width: 180},
            {field: "template", displayName: "巡检模板", width: 220},
            {field: "task_type", displayName: "任务类型", width: 200},
            {field: "create_time", displayName: "创建时间", width: 220},
            {
                displayName: "操作",
                cellTemplate: '<div style="width:100%;padding-top:5px;text-align: center">' +
                '<span style="cursor: pointer" class="btn btn-xs btn-danger" ui-sref="my_test({id:row.entity.id})">跳转</span>' +
                '</div>'
            }
        ]
    };

}]);