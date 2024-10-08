import types
from typing import Any, Callable, Iterable, overload

from _typeshed import Incomplete

SQLITE_ABORT: int
SQLITE_ABORT_ROLLBACK: int
SQLITE_ACCESS_EXISTS: int
SQLITE_ACCESS_READ: int
SQLITE_ACCESS_READWRITE: int
SQLITE_ALTER_TABLE: int
SQLITE_ANALYZE: int
SQLITE_ATTACH: int
SQLITE_AUTH: int
SQLITE_AUTH_USER: int
SQLITE_BUSY: int
SQLITE_BUSY_RECOVERY: int
SQLITE_BUSY_SNAPSHOT: int
SQLITE_BUSY_TIMEOUT: int
SQLITE_CANTOPEN: int
SQLITE_CANTOPEN_CONVPATH: int
SQLITE_CANTOPEN_DIRTYWAL: int
SQLITE_CANTOPEN_FULLPATH: int
SQLITE_CANTOPEN_ISDIR: int
SQLITE_CANTOPEN_NOTEMPDIR: int
SQLITE_CANTOPEN_SYMLINK: int
SQLITE_CHECKPOINT_FULL: int
SQLITE_CHECKPOINT_PASSIVE: int
SQLITE_CHECKPOINT_RESTART: int
SQLITE_CHECKPOINT_TRUNCATE: int
SQLITE_CONFIG_COVERING_INDEX_SCAN: int
SQLITE_CONFIG_GETMALLOC: int
SQLITE_CONFIG_GETMUTEX: int
SQLITE_CONFIG_GETPCACHE: int
SQLITE_CONFIG_GETPCACHE2: int
SQLITE_CONFIG_HEAP: int
SQLITE_CONFIG_LOG: int
SQLITE_CONFIG_LOOKASIDE: int
SQLITE_CONFIG_MALLOC: int
SQLITE_CONFIG_MEMDB_MAXSIZE: int
SQLITE_CONFIG_MEMSTATUS: int
SQLITE_CONFIG_MMAP_SIZE: int
SQLITE_CONFIG_MULTITHREAD: int
SQLITE_CONFIG_MUTEX: int
SQLITE_CONFIG_PAGECACHE: int
SQLITE_CONFIG_PCACHE: int
SQLITE_CONFIG_PCACHE2: int
SQLITE_CONFIG_PCACHE_HDRSZ: int
SQLITE_CONFIG_PMASZ: int
SQLITE_CONFIG_SCRATCH: int
SQLITE_CONFIG_SERIALIZED: int
SQLITE_CONFIG_SINGLETHREAD: int
SQLITE_CONFIG_SMALL_MALLOC: int
SQLITE_CONFIG_SORTERREF_SIZE: int
SQLITE_CONFIG_SQLLOG: int
SQLITE_CONFIG_STMTJRNL_SPILL: int
SQLITE_CONFIG_URI: int
SQLITE_CONFIG_WIN32_HEAPSIZE: int
SQLITE_CONSTRAINT: int
SQLITE_CONSTRAINT_CHECK: int
SQLITE_CONSTRAINT_COMMITHOOK: int
SQLITE_CONSTRAINT_DATATYPE: int
SQLITE_CONSTRAINT_FOREIGNKEY: int
SQLITE_CONSTRAINT_FUNCTION: int
SQLITE_CONSTRAINT_NOTNULL: int
SQLITE_CONSTRAINT_PINNED: int
SQLITE_CONSTRAINT_PRIMARYKEY: int
SQLITE_CONSTRAINT_ROWID: int
SQLITE_CONSTRAINT_TRIGGER: int
SQLITE_CONSTRAINT_UNIQUE: int
SQLITE_CONSTRAINT_VTAB: int
SQLITE_COPY: int
SQLITE_CORRUPT: int
SQLITE_CORRUPT_INDEX: int
SQLITE_CORRUPT_SEQUENCE: int
SQLITE_CORRUPT_VTAB: int
SQLITE_CREATE_INDEX: int
SQLITE_CREATE_TABLE: int
SQLITE_CREATE_TEMP_INDEX: int
SQLITE_CREATE_TEMP_TABLE: int
SQLITE_CREATE_TEMP_TRIGGER: int
SQLITE_CREATE_TEMP_VIEW: int
SQLITE_CREATE_TRIGGER: int
SQLITE_CREATE_VIEW: int
SQLITE_CREATE_VTABLE: int
SQLITE_DBCONFIG_DEFENSIVE: int
SQLITE_DBCONFIG_DQS_DDL: int
SQLITE_DBCONFIG_DQS_DML: int
SQLITE_DBCONFIG_ENABLE_FKEY: int
SQLITE_DBCONFIG_ENABLE_FTS3_TOKENIZER: int
SQLITE_DBCONFIG_ENABLE_LOAD_EXTENSION: int
SQLITE_DBCONFIG_ENABLE_QPSG: int
SQLITE_DBCONFIG_ENABLE_TRIGGER: int
SQLITE_DBCONFIG_ENABLE_VIEW: int
SQLITE_DBCONFIG_LEGACY_ALTER_TABLE: int
SQLITE_DBCONFIG_LEGACY_FILE_FORMAT: int
SQLITE_DBCONFIG_LOOKASIDE: int
SQLITE_DBCONFIG_MAINDBNAME: int
SQLITE_DBCONFIG_MAX: int
SQLITE_DBCONFIG_NO_CKPT_ON_CLOSE: int
SQLITE_DBCONFIG_RESET_DATABASE: int
SQLITE_DBCONFIG_REVERSE_SCANORDER: int
SQLITE_DBCONFIG_STMT_SCANSTATUS: int
SQLITE_DBCONFIG_TRIGGER_EQP: int
SQLITE_DBCONFIG_TRUSTED_SCHEMA: int
SQLITE_DBCONFIG_WRITABLE_SCHEMA: int
SQLITE_DBSTATUS_CACHE_HIT: int
SQLITE_DBSTATUS_CACHE_MISS: int
SQLITE_DBSTATUS_CACHE_SPILL: int
SQLITE_DBSTATUS_CACHE_USED: int
SQLITE_DBSTATUS_CACHE_USED_SHARED: int
SQLITE_DBSTATUS_CACHE_WRITE: int
SQLITE_DBSTATUS_DEFERRED_FKS: int
SQLITE_DBSTATUS_LOOKASIDE_HIT: int
SQLITE_DBSTATUS_LOOKASIDE_MISS_FULL: int
SQLITE_DBSTATUS_LOOKASIDE_MISS_SIZE: int
SQLITE_DBSTATUS_LOOKASIDE_USED: int
SQLITE_DBSTATUS_MAX: int
SQLITE_DBSTATUS_SCHEMA_USED: int
SQLITE_DBSTATUS_STMT_USED: int
SQLITE_DELETE: int
SQLITE_DENY: int
SQLITE_DETACH: int
SQLITE_DETERMINISTIC: int
SQLITE_DIRECTONLY: int
SQLITE_DONE: int
SQLITE_DROP_INDEX: int
SQLITE_DROP_TABLE: int
SQLITE_DROP_TEMP_INDEX: int
SQLITE_DROP_TEMP_TABLE: int
SQLITE_DROP_TEMP_TRIGGER: int
SQLITE_DROP_TEMP_VIEW: int
SQLITE_DROP_TRIGGER: int
SQLITE_DROP_VIEW: int
SQLITE_DROP_VTABLE: int
SQLITE_EMPTY: int
SQLITE_ERROR: int
SQLITE_ERROR_MISSING_COLLSEQ: int
SQLITE_ERROR_RETRY: int
SQLITE_ERROR_SNAPSHOT: int
SQLITE_FAIL: int
SQLITE_FCNTL_BEGIN_ATOMIC_WRITE: int
SQLITE_FCNTL_BUSYHANDLER: int
SQLITE_FCNTL_CHUNK_SIZE: int
SQLITE_FCNTL_CKPT_DONE: int
SQLITE_FCNTL_CKPT_START: int
SQLITE_FCNTL_CKSM_FILE: int
SQLITE_FCNTL_COMMIT_ATOMIC_WRITE: int
SQLITE_FCNTL_COMMIT_PHASETWO: int
SQLITE_FCNTL_DATA_VERSION: int
SQLITE_FCNTL_EXTERNAL_READER: int
SQLITE_FCNTL_FILE_POINTER: int
SQLITE_FCNTL_GET_LOCKPROXYFILE: int
SQLITE_FCNTL_HAS_MOVED: int
SQLITE_FCNTL_JOURNAL_POINTER: int
SQLITE_FCNTL_LAST_ERRNO: int
SQLITE_FCNTL_LOCKSTATE: int
SQLITE_FCNTL_LOCK_TIMEOUT: int
SQLITE_FCNTL_MMAP_SIZE: int
SQLITE_FCNTL_OVERWRITE: int
SQLITE_FCNTL_PDB: int
SQLITE_FCNTL_PERSIST_WAL: int
SQLITE_FCNTL_POWERSAFE_OVERWRITE: int
SQLITE_FCNTL_PRAGMA: int
SQLITE_FCNTL_RBU: int
SQLITE_FCNTL_RESERVE_BYTES: int
SQLITE_FCNTL_RESET_CACHE: int
SQLITE_FCNTL_ROLLBACK_ATOMIC_WRITE: int
SQLITE_FCNTL_SET_LOCKPROXYFILE: int
SQLITE_FCNTL_SIZE_HINT: int
SQLITE_FCNTL_SIZE_LIMIT: int
SQLITE_FCNTL_SYNC: int
SQLITE_FCNTL_SYNC_OMITTED: int
SQLITE_FCNTL_TEMPFILENAME: int
SQLITE_FCNTL_TRACE: int
SQLITE_FCNTL_VFSNAME: int
SQLITE_FCNTL_VFS_POINTER: int
SQLITE_FCNTL_WAL_BLOCK: int
SQLITE_FCNTL_WIN32_AV_RETRY: int
SQLITE_FCNTL_WIN32_GET_HANDLE: int
SQLITE_FCNTL_WIN32_SET_HANDLE: int
SQLITE_FCNTL_ZIPVFS: int
SQLITE_FORMAT: int
SQLITE_FULL: int
SQLITE_FUNCTION: int
SQLITE_IGNORE: int
SQLITE_INDEX_CONSTRAINT_EQ: int
SQLITE_INDEX_CONSTRAINT_FUNCTION: int
SQLITE_INDEX_CONSTRAINT_GE: int
SQLITE_INDEX_CONSTRAINT_GLOB: int
SQLITE_INDEX_CONSTRAINT_GT: int
SQLITE_INDEX_CONSTRAINT_IS: int
SQLITE_INDEX_CONSTRAINT_ISNOT: int
SQLITE_INDEX_CONSTRAINT_ISNOTNULL: int
SQLITE_INDEX_CONSTRAINT_ISNULL: int
SQLITE_INDEX_CONSTRAINT_LE: int
SQLITE_INDEX_CONSTRAINT_LIKE: int
SQLITE_INDEX_CONSTRAINT_LIMIT: int
SQLITE_INDEX_CONSTRAINT_LT: int
SQLITE_INDEX_CONSTRAINT_MATCH: int
SQLITE_INDEX_CONSTRAINT_NE: int
SQLITE_INDEX_CONSTRAINT_OFFSET: int
SQLITE_INDEX_CONSTRAINT_REGEXP: int
SQLITE_INDEX_SCAN_UNIQUE: int
SQLITE_INNOCUOUS: int
SQLITE_INSERT: int
SQLITE_INTERNAL: int
SQLITE_INTERRUPT: int
SQLITE_IOCAP_ATOMIC: int
SQLITE_IOCAP_ATOMIC16K: int
SQLITE_IOCAP_ATOMIC1K: int
SQLITE_IOCAP_ATOMIC2K: int
SQLITE_IOCAP_ATOMIC32K: int
SQLITE_IOCAP_ATOMIC4K: int
SQLITE_IOCAP_ATOMIC512: int
SQLITE_IOCAP_ATOMIC64K: int
SQLITE_IOCAP_ATOMIC8K: int
SQLITE_IOCAP_BATCH_ATOMIC: int
SQLITE_IOCAP_IMMUTABLE: int
SQLITE_IOCAP_POWERSAFE_OVERWRITE: int
SQLITE_IOCAP_SAFE_APPEND: int
SQLITE_IOCAP_SEQUENTIAL: int
SQLITE_IOCAP_UNDELETABLE_WHEN_OPEN: int
SQLITE_IOERR: int
SQLITE_IOERR_ACCESS: int
SQLITE_IOERR_AUTH: int
SQLITE_IOERR_BEGIN_ATOMIC: int
SQLITE_IOERR_BLOCKED: int
SQLITE_IOERR_CHECKRESERVEDLOCK: int
SQLITE_IOERR_CLOSE: int
SQLITE_IOERR_COMMIT_ATOMIC: int
SQLITE_IOERR_CONVPATH: int
SQLITE_IOERR_CORRUPTFS: int
SQLITE_IOERR_DATA: int
SQLITE_IOERR_DELETE: int
SQLITE_IOERR_DELETE_NOENT: int
SQLITE_IOERR_DIR_CLOSE: int
SQLITE_IOERR_DIR_FSYNC: int
SQLITE_IOERR_FSTAT: int
SQLITE_IOERR_FSYNC: int
SQLITE_IOERR_GETTEMPPATH: int
SQLITE_IOERR_IN_PAGE: int
SQLITE_IOERR_LOCK: int
SQLITE_IOERR_MMAP: int
SQLITE_IOERR_NOMEM: int
SQLITE_IOERR_RDLOCK: int
SQLITE_IOERR_READ: int
SQLITE_IOERR_ROLLBACK_ATOMIC: int
SQLITE_IOERR_SEEK: int
SQLITE_IOERR_SHMLOCK: int
SQLITE_IOERR_SHMMAP: int
SQLITE_IOERR_SHMOPEN: int
SQLITE_IOERR_SHMSIZE: int
SQLITE_IOERR_SHORT_READ: int
SQLITE_IOERR_TRUNCATE: int
SQLITE_IOERR_UNLOCK: int
SQLITE_IOERR_VNODE: int
SQLITE_IOERR_WRITE: int
SQLITE_LIMIT_ATTACHED: int
SQLITE_LIMIT_COLUMN: int
SQLITE_LIMIT_COMPOUND_SELECT: int
SQLITE_LIMIT_EXPR_DEPTH: int
SQLITE_LIMIT_FUNCTION_ARG: int
SQLITE_LIMIT_LENGTH: int
SQLITE_LIMIT_LIKE_PATTERN_LENGTH: int
SQLITE_LIMIT_SQL_LENGTH: int
SQLITE_LIMIT_TRIGGER_DEPTH: int
SQLITE_LIMIT_VARIABLE_NUMBER: int
SQLITE_LIMIT_VDBE_OP: int
SQLITE_LIMIT_WORKER_THREADS: int
SQLITE_LOCKED: int
SQLITE_LOCKED_SHAREDCACHE: int
SQLITE_LOCKED_VTAB: int
SQLITE_LOCK_EXCLUSIVE: int
SQLITE_LOCK_NONE: int
SQLITE_LOCK_PENDING: int
SQLITE_LOCK_RESERVED: int
SQLITE_LOCK_SHARED: int
SQLITE_MISMATCH: int
SQLITE_MISUSE: int
SQLITE_NOLFS: int
SQLITE_NOMEM: int
SQLITE_NOTADB: int
SQLITE_NOTFOUND: int
SQLITE_NOTICE: int
SQLITE_NOTICE_RBU: int
SQLITE_NOTICE_RECOVER_ROLLBACK: int
SQLITE_NOTICE_RECOVER_WAL: int
SQLITE_OK: int
SQLITE_OK_LOAD_PERMANENTLY: int
SQLITE_OK_SYMLINK: int
SQLITE_OPEN_AUTOPROXY: int
SQLITE_OPEN_CREATE: int
SQLITE_OPEN_DELETEONCLOSE: int
SQLITE_OPEN_EXCLUSIVE: int
SQLITE_OPEN_EXRESCODE: int
SQLITE_OPEN_FULLMUTEX: int
SQLITE_OPEN_MAIN_DB: int
SQLITE_OPEN_MAIN_JOURNAL: int
SQLITE_OPEN_MEMORY: int
SQLITE_OPEN_NOFOLLOW: int
SQLITE_OPEN_NOMUTEX: int
SQLITE_OPEN_PRIVATECACHE: int
SQLITE_OPEN_READONLY: int
SQLITE_OPEN_READWRITE: int
SQLITE_OPEN_SHAREDCACHE: int
SQLITE_OPEN_SUBJOURNAL: int
SQLITE_OPEN_SUPER_JOURNAL: int
SQLITE_OPEN_TEMP_DB: int
SQLITE_OPEN_TEMP_JOURNAL: int
SQLITE_OPEN_TRANSIENT_DB: int
SQLITE_OPEN_URI: int
SQLITE_OPEN_WAL: int
SQLITE_PERM: int
SQLITE_PRAGMA: int
SQLITE_PREPARE_NORMALIZE: int
SQLITE_PREPARE_NO_VTAB: int
SQLITE_PREPARE_PERSISTENT: int
SQLITE_PROTOCOL: int
SQLITE_RANGE: int
SQLITE_READ: int
SQLITE_READONLY: int
SQLITE_READONLY_CANTINIT: int
SQLITE_READONLY_CANTLOCK: int
SQLITE_READONLY_DBMOVED: int
SQLITE_READONLY_DIRECTORY: int
SQLITE_READONLY_RECOVERY: int
SQLITE_READONLY_ROLLBACK: int
SQLITE_RECURSIVE: int
SQLITE_REINDEX: int
SQLITE_REPLACE: int
SQLITE_RESULT_SUBTYPE: int
SQLITE_ROLLBACK: int
SQLITE_ROW: int
SQLITE_SAVEPOINT: int
SQLITE_SCHEMA: int
SQLITE_SELECT: int
SQLITE_SHM_EXCLUSIVE: int
SQLITE_SHM_LOCK: int
SQLITE_SHM_SHARED: int
SQLITE_SHM_UNLOCK: int
SQLITE_STATUS_MALLOC_COUNT: int
SQLITE_STATUS_MALLOC_SIZE: int
SQLITE_STATUS_MEMORY_USED: int
SQLITE_STATUS_PAGECACHE_OVERFLOW: int
SQLITE_STATUS_PAGECACHE_SIZE: int
SQLITE_STATUS_PAGECACHE_USED: int
SQLITE_STATUS_PARSER_STACK: int
SQLITE_STATUS_SCRATCH_OVERFLOW: int
SQLITE_STATUS_SCRATCH_SIZE: int
SQLITE_STATUS_SCRATCH_USED: int
SQLITE_STMTSTATUS_AUTOINDEX: int
SQLITE_STMTSTATUS_FILTER_HIT: int
SQLITE_STMTSTATUS_FILTER_MISS: int
SQLITE_STMTSTATUS_FULLSCAN_STEP: int
SQLITE_STMTSTATUS_MEMUSED: int
SQLITE_STMTSTATUS_REPREPARE: int
SQLITE_STMTSTATUS_RUN: int
SQLITE_STMTSTATUS_SORT: int
SQLITE_STMTSTATUS_VM_STEP: int
SQLITE_SUBTYPE: int
SQLITE_SYNC_DATAONLY: int
SQLITE_SYNC_FULL: int
SQLITE_SYNC_NORMAL: int
SQLITE_TOOBIG: int
SQLITE_TRACE_CLOSE: int
SQLITE_TRACE_PROFILE: int
SQLITE_TRACE_ROW: int
SQLITE_TRACE_STMT: int
SQLITE_TRANSACTION: int
SQLITE_TXN_NONE: int
SQLITE_TXN_READ: int
SQLITE_TXN_WRITE: int
SQLITE_UPDATE: int
SQLITE_VERSION_NUMBER: int
SQLITE_VTAB_CONSTRAINT_SUPPORT: int
SQLITE_VTAB_DIRECTONLY: int
SQLITE_VTAB_INNOCUOUS: int
SQLITE_VTAB_USES_ALL_SCHEMAS: int
SQLITE_WARNING: int
SQLITE_WARNING_AUTOINDEX: int
compile_options: tuple
connection_hooks: list
keywords: set
mapping_access: dict
mapping_authorizer_function: dict
mapping_authorizer_return_codes: dict
mapping_bestindex_constraints: dict
mapping_config: dict
mapping_conflict_resolution_modes: dict
mapping_db_config: dict
mapping_db_status: dict
mapping_device_characteristics: dict
mapping_extended_result_codes: dict
mapping_file_control: dict
mapping_function_flags: dict
mapping_limits: dict
mapping_locking_level: dict
mapping_open_flags: dict
mapping_prepare_flags: dict
mapping_result_codes: dict
mapping_statement_status: dict
mapping_status: dict
mapping_sync: dict
mapping_trace_codes: dict
mapping_txn_state: dict
mapping_virtual_table_configuration_options: dict
mapping_virtual_table_scan_flags: dict
mapping_wal_checkpoint: dict
mapping_xshmlock_flags: dict
using_amalgamation: bool
class AbortError(Error): ...

class AuthError(Error): ...

class Backup:
    done: Incomplete
    page_count: Incomplete
    pagecount: Any
    remaining: Incomplete
    def close(self, force: bool = ...) -> None: ...
    def finish(self) -> None: ...
    def step(self, npages: int = ...) -> bool: ...
    def __enter__(self) -> Backup: ...
    def __exit__(self, etype: type[BaseException] | None, evalue: BaseException | None, etraceback: types.TracebackType | None) -> bool | None: ...

class BindingsError(Error): ...

class Blob:
    def close(self, force: bool = ...) -> None: ...
    def length(self) -> int: ...
    def read(self, length: int = ...) -> bytes: ...
    def read_into(self, buffer, offset: int = ..., length: int = ...) -> None: ...
    def readinto(self, *args :Any, **kwargs:Any): ...
    def reopen(self, rowid: int) -> None: ...
    def seek(self, offset: int, whence: int = ...) -> None: ...
    def tell(self) -> int: ...
    def write(self, data: bytes) -> None: ...
    def __enter__(self) -> Blob: ...
    def __exit__(self, etype: type[BaseException] | None, evalue: BaseException | None, etraceback: types.TracebackType | None) -> bool | None: ...

class BusyError(Error): ...

class CantOpenError(Error): ...

class Connection:
    authorizer: Incomplete
    cursor_factory: Incomplete
    exec_trace: Incomplete
    exectrace: Any
    filename: Incomplete
    filename_journal: Incomplete
    filename_wal: Incomplete
    in_transaction: Incomplete
    is_interrupted: Incomplete
    open_flags: Incomplete
    open_vfs: Incomplete
    row_trace: Incomplete
    rowtrace: Any
    system_errno: Incomplete
    def __init__(self, *args :Any, **kwargs:Any) -> None: ...
    def autovacuum_pages(self, callable: Callable[[str, int, int, int], int] | None) -> None: ...
    def backup(self, databasename: str, sourceconnection: Connection, sourcedatabasename: str) -> Backup: ...
    def blob_open(self, database: str, table: str, column: str, rowid: int, writeable: bool) -> Blob: ...
    def blobopen(self, *args :Any, **kwargs:Any): ...
    def cache_flush(self) -> None: ...
    def cache_stats(self, include_entries: bool = ...) -> dict[str, int]: ...
    def cacheflush(self, *args :Any, **kwargs:Any): ...
    def changes(self) -> int: ...
    def close(self, force: bool = ...) -> None: ...
    def collation_needed(self, callable: Callable[[Connection, str], None] | None) -> None: ...
    def collationneeded(self, *args :Any, **kwargs:Any): ...
    def column_metadata(self, dbname: str | None, table_name: str, column_name: str) -> tuple[str, str, bool, bool, bool]: ...
    def config(self, op: int, *args: int) -> int: ...
    def create_aggregate_function(self, *args :Any, **kwargs:Any): ...
    def create_collation(self, name: str, callback: Callable[[str, str], int] | None) -> None: ...
    def create_module(self, *args :Any, **kwargs:Any): ...
    def create_scalar_function(self, *args :Any, **kwargs:Any): ...
    def create_window_function(self, *args :Any, **kwargs:Any): ...
    def createaggregatefunction(self, *args :Any, **kwargs:Any): ...
    def createcollation(self, *args :Any, **kwargs:Any): ...
    def createmodule(self, *args :Any, **kwargs:Any): ...
    def createscalarfunction(self, *args :Any, **kwargs:Any): ...
    def cursor(self) -> Cursor: ...
    def db_filename(self, name: str) -> str: ...
    def db_names(self) -> list[str]: ...
    def deserialize(self, name: str, contents: bytes) -> None: ...
    def drop_modules(self, keep: Iterable[str] | None) -> None: ...
    def enable_load_extension(self, enable: bool) -> None: ...
    def enableloadextension(self, *args :Any, **kwargs:Any): ...
    def execute(self, *args :Any, **kwargs:Any): ...
    def executemany(self, *args :Any, **kwargs:Any): ...
    def file_control(self, dbname: str, op: int, pointer: int) -> bool: ...
    def filecontrol(self, *args :Any, **kwargs:Any): ...
    def get_autocommit(self) -> bool: ...
    def get_exec_trace(self) -> ExecTracer | None: ...
    def get_row_trace(self) -> RowTracer | None: ...
    def getautocommit(self, *args :Any, **kwargs:Any): ...
    def getexectrace(self, *args :Any, **kwargs:Any): ...
    def getrowtrace(self, *args :Any, **kwargs:Any): ...
    def interrupt(self) -> None: ...
    def last_insert_rowid(self) -> int: ...
    def limit(self, id: int, newval: int = ...) -> int: ...
    def load_extension(self, filename: str, entrypoint: str | None = ...) -> None: ...
    def loadextension(self, *args :Any, **kwargs:Any): ...
    def overload_function(self, name: str, nargs: int) -> None: ...
    def overloadfunction(self, *args :Any, **kwargs:Any): ...
    def pragma(self, withthevalueifsupplied) -> Any: ...
    def read(self, schema: str, which: int, offset: int, amount: int) -> tuple[bool, bytes]: ...
    def readonly(self, name: str) -> bool: ...
    def release_memory(self) -> None: ...
    def serialize(self, name: str) -> bytes: ...
    def set_authorizer(self, callable: Authorizer | None) -> None: ...
    def set_busy_handler(self, callable: Callable[[int], bool] | None) -> None: ...
    def set_busy_timeout(self, milliseconds: int) -> None: ...
    def set_commit_hook(self, callable: CommitHook | None) -> None: ...
    def set_exec_trace(self, callable: ExecTracer | None) -> None: ...
    def set_last_insert_rowid(self, rowid: int) -> None: ...
    def set_profile(self, callable: Callable[[str, int], None] | None) -> None: ...
    def set_progress_handler(self, callable: Callable[[], bool] | None, nsteps: int = ...) -> None: ...
    def set_rollback_hook(self, callable: Callable[[], None] | None) -> None: ...
    def set_row_trace(self, callable: RowTracer | None) -> None: ...
    def set_update_hook(self, callable: Callable[[int, str, str, int], None] | None) -> None: ...
    def set_wal_hook(self, callable: Callable[[Connection, str, int], int] | None) -> None: ...
    def setauthorizer(self, *args :Any, **kwargs:Any): ...
    def setbusyhandler(self, *args :Any, **kwargs:Any): ...
    def setbusytimeout(self, *args :Any, **kwargs:Any): ...
    def setcommithook(self, *args :Any, **kwargs:Any): ...
    def setexectrace(self, *args :Any, **kwargs:Any): ...
    def setprofile(self, *args :Any, **kwargs:Any): ...
    def setprogresshandler(self, *args :Any, **kwargs:Any): ...
    def setrollbackhook(self, *args :Any, **kwargs:Any): ...
    def setrowtrace(self, *args :Any, **kwargs:Any): ...
    def setupdatehook(self, *args :Any, **kwargs:Any): ...
    def setwalhook(self, *args :Any, **kwargs:Any): ...
    def sqlite3_pointer(self) -> int: ...
    def sqlite3pointer(self, *args :Any, **kwargs:Any): ...
    def status(self, op: int, reset: bool = ...) -> tuple[int, int]: ...
    def table_exists(self, dbname: str | None, table_name: str) -> bool: ...
    def total_changes(self) -> int: ...
    def totalchanges(self, *args :Any, **kwargs:Any): ...
    def trace_v2(self, mask: int, callback: Callable[[dict], None] | None = ...) -> None: ...
    def txn_state(self, schema: str | None = ...) -> int: ...
    def vfsname(self, *args :Any, **kwargs:Any): ...
    def vtab_config(self, op: int, val: int = ...) -> None: ...
    def vtab_on_conflict(self) -> int: ...
    def wal_autocheckpoint(self, n: int) -> None: ...
    def wal_checkpoint(self, dbname: str | None = ..., mode: int = ...) -> tuple[int, int]: ...
    def __enter__(self) -> Connection: ...
    def __exit__(self, etype: type[BaseException] | None, evalue: BaseException | None, etraceback: types.TracebackType | None) -> bool | None: ...

class ConnectionClosedError(Error): ...

class ConnectionNotClosedError(Error): ...

class ConstraintError(Error): ...

class CorruptError(Error): ...

class Cursor:
    bindings_count: Incomplete
    bindings_names: Incomplete
    connection: Incomplete
    description: Incomplete
    description_full: Incomplete
    exec_trace: Incomplete
    exectrace: Any
    expanded_sql: Incomplete
    get: Incomplete
    has_vdbe: Incomplete
    is_explain: Incomplete
    is_readonly: Incomplete
    row_trace: Incomplete
    rowtrace: Any
    def __init__(self, *args :Any, **kwargs:Any) -> None: ...
    def close(self, force: bool = ...) -> None: ...
    def execute(self, *args :Any, **kwargs:Any): ...
    def executemany(self, *args :Any, **kwargs:Any): ...
    def fetchall(self, *args :Any, **kwargs:Any) -> list[tuple[SQLiteValue, ...]]: ...
    def fetchone(self) -> Any | None: ...
    def get_connection(self) -> Connection: ...
    def get_description(self, *args :Any, **kwargs:Any): ...
    def get_exec_trace(self) -> ExecTracer | None: ...
    def get_row_trace(self) -> RowTracer | None: ...
    def getconnection(self, *args :Any, **kwargs:Any): ...
    def getdescription(self, *args :Any, **kwargs:Any): ...
    def getexectrace(self, *args :Any, **kwargs:Any): ...
    def getrowtrace(self, *args :Any, **kwargs:Any): ...
    def set_exec_trace(self, callable: ExecTracer | None) -> None: ...
    def set_row_trace(self, callable: RowTracer | None) -> None: ...
    def setexectrace(self, *args :Any, **kwargs:Any): ...
    def setrowtrace(self, *args :Any, **kwargs:Any): ...
    def __iter__(self): ...
    def __next__(self): ...

class CursorClosedError(Error): ...

class EmptyError(Error): ...

class Error(Exception): ...

class ExecTraceAbort(Error): ...

class ExecutionCompleteError(Error): ...

class ExtensionLoadingError(Error): ...

class ForkingViolationError(Error): ...

class FormatError(Error): ...

class FullError(Error): ...

class IOError(Error): ...

class IncompleteExecutionError(Error): ...

class IndexInfo:
    colUsed: Incomplete
    distinct: Incomplete
    estimatedCost: Incomplete
    estimatedRows: Incomplete
    idxFlags: Incomplete
    idxNum: Incomplete
    idxStr: Incomplete
    nConstraint: Incomplete
    nOrderBy: Incomplete
    orderByConsumed: Incomplete
    def get_aConstraintUsage_argvIndex(self, which: int) -> int: ...
    def get_aConstraintUsage_in(self, which: int) -> bool: ...
    def get_aConstraintUsage_omit(self, which: int) -> bool: ...
    def get_aConstraint_collation(self, which: int) -> str: ...
    def get_aConstraint_iColumn(self, which: int) -> int: ...
    def get_aConstraint_op(self, which: int) -> int: ...
    def get_aConstraint_rhs(self, which: int) -> SQLiteValue: ...
    def get_aConstraint_usable(self, which: int) -> bool: ...
    def get_aOrderBy_desc(self, which: int) -> bool: ...
    def get_aOrderBy_iColumn(self, which: int) -> int: ...
    def set_aConstraintUsage_argvIndex(self, which: int, argvIndex: int) -> None: ...
    def set_aConstraintUsage_in(self, which: int, filter_all: bool) -> None: ...
    def set_aConstraintUsage_omit(self, which: int, omit: bool) -> None: ...

class InternalError(Error): ...

class InterruptError(Error): ...

class LockedError(Error): ...

class MismatchError(Error): ...

class MisuseError(Error): ...

class NoLFSError(Error): ...

class NoMemError(Error): ...

class NotADBError(Error): ...

class NotFoundError(Error): ...

class PermissionsError(Error): ...

class ProtocolError(Error): ...

class RangeError(Error): ...

class ReadOnlyError(Error): ...

class SQLError(Error): ...

class SchemaChangeError(Error): ...

class ThreadingViolationError(Error): ...

class TooBigError(Error): ...

class URIFilename:
    parameters: Incomplete
    def filename(self) -> str: ...
    def uri_boolean(self, name: str, default: bool) -> bool: ...
    def uri_int(self, name: str, default: int) -> int: ...
    def uri_parameter(self, name: str) -> str | None: ...

class VFS:
    def __init__(self, *args :Any, **kwargs:Any) -> None: ...
    def excepthook(self, etype: type[BaseException], evalue: BaseException, etraceback: types.TracebackType | None) -> Any: ...
    def unregister(self) -> None: ...
    def xAccess(self, pathname: str, flags: int) -> bool: ...
    def xCurrentTime(self) -> float: ...
    def xCurrentTimeInt64(self) -> int: ...
    def xDelete(self, filename: str, syncdir: bool) -> None: ...
    @overload
    def xDlClose(self, handle: int) -> None: ...
    @overload
    def xDlClose(self, handle: int) -> Any: ...
    def xDlError(self) -> str: ...
    @overload
    def xDlOpen(self, filename: str) -> int: ...
    @overload
    def xDlOpen(self, name: str) -> Any: ...
    @overload
    def xDlSym(self, handle: int, symbol: str) -> int: ...
    @overload
    def xDlSym(self, ptr: int, name: str) -> Any: ...
    def xFullPathname(self, name: str) -> str: ...
    def xGetLastError(self) -> tuple[int, str]: ...
    def xGetSystemCall(self, name: str) -> int | None: ...
    def xNextSystemCall(self, name: str | None) -> str | None: ...
    def xOpen(self, name, flags: list[int, int]) -> VFSFile: ...
    def xRandomness(self, numbytes: int) -> bytes: ...
    def xSetSystemCall(self, name: str | None, pointer: int) -> bool: ...
    def xSleep(self, microseconds: int) -> int: ...

class VFSFcntlPragma:
    name: Incomplete
    result: Incomplete
    value: Incomplete
    def __init__(self, *args :Any, **kwargs:Any) -> None: ...

class VFSFile:
    def __init__(self, *args :Any, **kwargs:Any) -> None: ...
    def excepthook(self, etype: type[BaseException], evalue: BaseException, etraceback: types.TracebackType | None) -> None: ...
    def xCheckReservedLock(self) -> bool: ...
    def xClose(self) -> None: ...
    def xDeviceCharacteristics(self) -> int: ...
    def xFileControl(self, *args :Any, **kwargs:Any): ...
    def xFileSize(self) -> int: ...
    def xLock(self, level: int) -> None: ...
    def xRead(self, amount: int, offset: int) -> bytes: ...
    def xSectorSize(self) -> int: ...
    def xSync(self, flags: int) -> None: ...
    def xTruncate(self, newsize: int) -> None: ...
    def xUnlock(self, level: int) -> None: ...
    def xWrite(self, data: bytes, offset: int) -> None: ...

class VFSFileClosedError(Error): ...

class VFSNotImplementedError(Error): ...

class no_change: ...

class zeroblob:
    def __init__(self, *args :Any, **kwargs:Any) -> None: ...
    def length(self) -> int: ...

def __getattr__(*args, **kwargs): ...
def allow_missing_dict_bindings(value: bool) -> bool: ...
def apsw_version() -> str: ...
def apswversion(*args, **kwargs): ...
@overload
def complete(statement: str) -> bool: ...
@overload
def complete(statement) -> Any: ...
def config(op: int, *args: Any) -> None: ...
def connections() -> list[Connection]: ...
def enable_shared_cache(enable: bool) -> None: ...
def enablesharedcache(*args, **kwargs): ...
def exception_for(code: int) -> Exception: ...
def exceptionfor(*args, **kwargs): ...
def format_sql_value(value: SQLiteValue) -> str: ...
def hard_heap_limit(limit: int) -> int: ...
def initialize() -> None: ...
def log(errorcode: int, message: str) -> None: ...
def memory_high_water(reset: bool = ...) -> int: ...
def memory_used() -> int: ...
def memoryhighwater(*args, **kwargs): ...
def memoryused(*args, **kwargs): ...
def randomness(amount: int) -> bytes: ...
def release_memory(amount: int) -> int: ...
def releasememory(*args, **kwargs): ...
def set_default_vfs(name: str) -> None: ...
def shutdown() -> None: ...
def sleep(milliseconds: int) -> int: ...
def soft_heap_limit(limit: int) -> int: ...
def softheaplimit(*args, **kwargs): ...
def sqlite3_sourceid() -> str: ...
def sqlite_lib_version() -> str: ...
def sqlitelibversion(*args, **kwargs): ...
def status(op: int, reset: bool = ...) -> tuple[int, int]: ...
def strglob(glob: str, string: str) -> int: ...
def stricmp(string1: str, string2: str) -> int: ...
def strlike(glob: str, string: str, escape: int = ...) -> int: ...
def strnicmp(string1: str, string2: str, count: int) -> int: ...
def unregister_vfs(name: str) -> None: ...
def vfs_details(*args, **kwargs): ...
def vfs_names() -> list[str]: ...
def vfsnames(*args, **kwargs): ...
