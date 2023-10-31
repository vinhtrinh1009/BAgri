import 'package:flutter_base/models/entities/garden_task/garden_task.dart';
import 'package:flutter_base/models/entities/garden_task/garden_task_detail.dart';
import 'package:flutter_base/models/entities/garden_task/task_delete_entity.dart';
import 'package:flutter_base/models/entities/task/task.dart';
import 'package:flutter_base/models/params/task/create_task_params.dart';
import 'package:flutter_base/models/response/object_response.dart';
import 'package:flutter_base/network/api_client_bagri.dart';

abstract class TaskRepository {
  Future<ObjectResponse<TaskListData>> getListTask();

  Future<ObjectResponse<GardenTaskList>> getGardenTask(
      String? seasonId, String? date);

  Future<dynamic> createTask({CreateTaskParam? param});

  Future<dynamic> updateTask({String? taskId, CreateTaskParam? param});

  Future<ObjectResponse<GardenTaskDetailResponse>> getTaskById(String taskId);

  Future<ObjectResponse<TaskDeleteEntity>> deleteTask(String taskId);
}

class TaskRepositoryImpl extends TaskRepository {
  ApiClient? _apiClient;

  TaskRepositoryImpl(ApiClient? client) {
    _apiClient = client;
  }

  @override
  Future<ObjectResponse<TaskListData>> getListTask() async {
    return await _apiClient!.getListTask();
  }

  @override
  Future<ObjectResponse<GardenTaskList>> getGardenTask(
      String? seasonId, String? date) async {
    return await _apiClient!.getGardenTask(seasonId!, date!);
  }

  @override
  Future<dynamic> createTask({CreateTaskParam? param}) {
    final body = {
      "step_id": param?.step_id ?? "",
      "farmer_ids": param?.farmer_ids,
      "description": param?.description,
      "manager_id": param?.manager_id,
      "season_id": param?.season_id,
      "name": param?.name,
      "date": param?.date,
      "start_time": param?.start_time ?? "",
      "end_time": param?.end_time ?? "",
      "result": param?.result ?? [],
      "items": param?.items ?? "",
    };

    return _apiClient!.createTask(body);
  }

  Future<dynamic> updateTask({String? taskId, CreateTaskParam? param}) {
    final body = {
      "step_id": param?.step_id ?? "",
      "farmer_ids": param?.farmer_ids,
      "description": param?.description,
      "manager_id": param?.manager_id,
      "season_id": param?.season_id,
      "name": param?.name,
      "date": param?.date,
      "start_time": param?.start_time ?? "",
      "end_time": param?.end_time ?? "",
      "result": param?.result ?? [],
      "items": param?.items ?? "",
    };
    return _apiClient!.updateTask(taskId, body);
  }

  @override
  Future<ObjectResponse<GardenTaskDetailResponse>> getTaskById(
      String taskId) async {
    return await _apiClient!.getTaskById(taskId);
  }

  @override
  Future<ObjectResponse<TaskDeleteEntity>> deleteTask(String taskId) async {
    return await _apiClient!.deleteTask(taskId);
  }
}
