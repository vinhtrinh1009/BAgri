import 'package:flutter_base/models/entities/process/list_process.dart';
import 'package:flutter_base/models/entities/process/process_delete.dart';
import 'package:flutter_base/models/entities/process/process_detail.dart';
import 'package:flutter_base/models/params/process/create_process_params.dart';
import 'package:flutter_base/models/response/object_response.dart';
import 'package:flutter_base/network/api_client_bagri.dart';

abstract class ProcessRepository {
  Future<ListProcessResponse> getListProcessData();

  Future<ProcessDeleteResponse> deleteProcess({String? processId});

  Future<dynamic> createProcess({CreateProcessParam? param});

  Future<dynamic> updateProcess({String? processId, CreateProcessParam? param});

  Future<ObjectResponse<ProcessDetailResponse>> getProcessById(
      String processId);

  Future<ListProcessResponse> getProcessOfTree(String treeId);
}

class ProcessRepositoryImpl extends ProcessRepository {
  ApiClient? _apiClient;

  ProcessRepositoryImpl(ApiClient? client) {
    _apiClient = client;
  }

  @override
  Future<ListProcessResponse> getListProcessData() async {
    return await _apiClient!.getListProcessData({});
  }

  Future<ProcessDeleteResponse> deleteProcess({String? processId}) async {
    return await _apiClient!.deleteProcess(processId: processId);
  }

  Future<dynamic> createProcess({CreateProcessParam? param}) {
    final body = {
      "name": param?.name ?? "",
      "tree_ids": param?.tree_ids ?? [],
      "stages": param?.stages ?? [],
    };

    return _apiClient!.createProcess(body);
  }

  Future<dynamic> updateProcess(
      {String? processId, CreateProcessParam? param}) {
    final body = {
      "name": param?.name ?? "",
      "tree_ids": param?.tree_ids ?? [],
      "stages": param?.stages ?? [],
    };
    return _apiClient!.updateProcess(processId, body);
  }

  @override
  Future<ObjectResponse<ProcessDetailResponse>> getProcessById(
      String processId) async {
    return await _apiClient!.getProcessById(processId);
  }

  @override
  Future<ListProcessResponse> getProcessOfTree(String treeId) async {
    return await _apiClient!.getProcessOfTree(treeId);
  }
}
