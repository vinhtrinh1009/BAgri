import 'package:flutter_base/models/entities/tree/list_tree_response.dart';
import 'package:flutter_base/models/entities/tree/tree_delete_response.dart';
import 'package:flutter_base/models/entities/tree/tree_detail_response.dart';
import 'package:flutter_base/models/params/trees/create_tree_params.dart';
import 'package:flutter_base/models/response/object_response.dart';
import 'package:flutter_base/network/api_client_bagri.dart';

abstract class TreeRepository {
  Future<ListTreeResponse> getListTreeData();

  Future<TreeDeleteResponse> deleteTree({String? treeId});

  Future<dynamic> createTree({CreateTreeParam? param});

  Future<dynamic> updateTree({String? treeId, CreateTreeParam? param});

  Future<ObjectResponse<TreeDetailResponse>> getTreeById(String treeId);
}

class TreeRepositoryImpl extends TreeRepository {
  ApiClient? _apiClient;

  TreeRepositoryImpl(ApiClient? client) {
    _apiClient = client;
  }

  @override
  Future<ListTreeResponse> getListTreeData() async {
    return await _apiClient!.getListTreeData({});
  }

  Future<TreeDeleteResponse> deleteTree({String? treeId}) async {
    return await _apiClient!.deleteTree(treeId: treeId);
  }

  Future<dynamic> createTree({CreateTreeParam? param}) {
    final body = {
      "name": param?.name ?? "",
      "description": param?.description ?? "",
    };

    return _apiClient!.createTree(body);
  }

  Future<dynamic> updateTree({String? treeId, CreateTreeParam? param}) {
    final body = {
      "name": param?.name ?? "",
      "description": param?.description ?? "",
    };
    return _apiClient!.updateTree(treeId, body);
  }

  @override
  Future<ObjectResponse<TreeDetailResponse>> getTreeById(String treeId) async {
    return await _apiClient!.getTreeById(treeId);
  }
}
