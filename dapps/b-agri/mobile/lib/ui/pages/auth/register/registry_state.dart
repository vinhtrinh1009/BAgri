part of 'registry_cubit.dart';

class RegistryState extends Equatable {
  LoadStatus? RegisterStatus;
  String? username;
  String? password;
  String? phone;
  RoleEntity? role;
  String? fullName;
  String? messageError;
  @override
  List<Object?> get props => [
        this.RegisterStatus,
        this.username,
        this.password,
        this.role,
        this.phone,
        this.fullName,
        this.messageError
      ];

  RegistryState({
    this.RegisterStatus,
    this.username,
    this.password,
    this.phone,
    this.role,
    this.fullName,
    this.messageError,
  });

  RegistryState copyWith({
    LoadStatus? RegisterStatus,
    String? username,
    String? password,
    String? phone,
    RoleEntity? role,
    String? fullName,
    String? messageError,
  }) {
    return RegistryState(
      RegisterStatus: RegisterStatus ?? this.RegisterStatus,
      username: username ?? this.username,
      password: password ?? this.password,
      phone: phone ?? this.phone,
      role: role ?? this.role,
      fullName: fullName ?? this.fullName,
      messageError: messageError ?? this.messageError,
    );
  }
}
