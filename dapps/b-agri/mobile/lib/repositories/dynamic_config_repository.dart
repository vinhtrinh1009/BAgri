import 'package:flutter_base/models/entities/config/dynamic_config_entity.dart';
import 'package:flutter_base/network/api_client_bagri.dart';

// DataFlow: Step 4
// Create repository

abstract class DynamicConfigRepository {
  // Future<List<DynamicConfigEntity>> getDynamicConfig();
}

class DynamicConfigRepositoryImpl extends DynamicConfigRepository {
  ApiClient? _apiClient;

  DynamicConfigRepositoryImpl(ApiClient? client) {
    _apiClient = client;
  }

  // @override
  // Future<List<DynamicConfigEntity>> getDynamicConfig() async {
  //   try {
  //     return await _apiClient!.getDynamicConfig();
  //   } catch (error) {
  //     throw error;
  //   }
  // }
}
