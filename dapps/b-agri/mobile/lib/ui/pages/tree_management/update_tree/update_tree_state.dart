part of 'update_tree_cubit.dart';

class UpdateTreeState extends Equatable {
  String? name;
  String? description;
  LoadStatus? updateTreeStatus;
  LoadStatus? loadStatus;
  TreeEntity? treeData;

  @override
  List<Object?> get props => [
        this.name,
        this.description,
        this.updateTreeStatus,
        this.loadStatus,
        this.treeData
      ];

  UpdateTreeState({
    this.name,
    this.description,
    this.updateTreeStatus,
    this.loadStatus,
    this.treeData,
  });

  UpdateTreeState copyWith({
    String? name,
    String? description,
    LoadStatus? updateTreeStatus,
    LoadStatus? loadStatus,
    TreeEntity? treeData,
  }) {
    return UpdateTreeState(
      name: name ?? this.name,
      description: description ?? this.description,
      updateTreeStatus: updateTreeStatus ?? this.updateTreeStatus,
      loadStatus: loadStatus ?? this.loadStatus,
      treeData: treeData ?? this.treeData,
    );
  }
}
