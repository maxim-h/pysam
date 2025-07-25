import array
import sys
from typing import (
    Any,
    Dict,
    Type,
    NamedTuple,
    Tuple,
    Optional,
    Sequence,
    Union,
    Callable,
    List,
    Literal,
    Iterable,
)

from pysam.libchtslib import HTSFile, _HasFileNo
from pysam.libcalignedsegment import AlignedSegment, PileupColumn
from pysam.libcfaidx import FastaFile

class IndexStats(NamedTuple):
    contig: str
    mapped: int
    unmapped: int
    total: int

VALID_HEADER_TYPES: Dict[str, Type]
VALID_HEADERS: Tuple[str]
KNOWN_HEADER_FIELDS: Dict[str, Dict[str, Type]]
VALID_HEADER_ORDER: Dict[str, Tuple[str]]

def build_header_line(fields: Dict[str, str], record: str) -> str: ...

class AlignmentHeader:
    def __init__(self) -> None: ...
    @classmethod
    def _from_text_and_lengths(
        cls,
        text: Optional[str],
        reference_names: Optional[Sequence[str]],
        reference_lengths: Optional[Sequence[int]],
    ) -> AlignmentHeader: ...
    @classmethod
    def from_text(cls, text: str) -> AlignmentHeader: ...
    @classmethod
    def from_dict(cls, header_dict: Dict) -> AlignmentHeader: ...
    @classmethod
    def from_references(
        cls,
        reference_names: Sequence[str],
        reference_lengths: Sequence[int],
        text: Optional[str] = ...,
        add_sq_text: bool = ...,
    ) -> AlignmentHeader: ...
    def __bool__(self) -> bool: ...
    def copy(self) -> AlignmentHeader: ...
    @property
    def nreferences(self) -> int: ...
    @property
    def references(self) -> Tuple[str]: ...
    @property
    def lengths(self) -> Tuple[int]: ...
    def to_dict(self) -> Dict: ...
    def get_reference_name(self, tid: int) -> Optional[str]: ...
    def get_reference_length(self, reference: str) -> int: ...
    def is_valid_tid(self, tid: int) -> bool: ...
    def get_tid(self, reference: str) -> int: ...

# The iterator produced by AlignmentFile is currently itself, but this may
# change in future and code should not make assumptions about this type.
AlignmentFileIterator = AlignmentFile

class AlignmentFile(HTSFile):
    def __init__(
        self,
        filename: Union[str, bytes, int, _HasFileNo],
        mode: Optional[
            Literal["r", "w", "wh", "rb", "wb", "wbu", "wb0", "rc", "wc"]
        ] = ...,
        template: Optional[AlignmentFile] = ...,
        reference_names: Optional[Sequence[str]] = ...,
        reference_lengths: Optional[Sequence[int]] = ...,
        reference_filename: Optional[str] = ...,
        text: Optional[str] = ...,
        header: Union[None, Dict, AlignmentHeader] = ...,
        add_sq_text: bool = ...,
        add_sam_header: bool = ...,
        check_sq: bool = ...,
        index_filename: Optional[str] = ...,
        filepath_index: Optional[str] = ...,
        require_index: bool = ...,
        duplicate_filehandle: bool = ...,
        ignore_truncation: bool = ...,
        format_options: Optional[Sequence[str]] = ...,
        threads: int = ...,
    ) -> None: ...
    def has_index(self) -> bool: ...
    def check_index(self) -> bool: ...
    def fetch(
        self,
        contig: Optional[str] = ...,
        start: Optional[int] = ...,
        stop: Optional[int] = ...,
        region: Optional[str] = ...,
        tid: Optional[int] = ...,
        until_eof: bool = ...,
        multiple_iterators: bool = ...,
        reference: Optional[str] = ...,
        end: int = ...,
    ) -> IteratorRow: ...
    def head(self, n: int, multiple_iterators: bool = ...) -> IteratorRow: ...
    def mate(self, read: AlignedSegment) -> AlignedSegment: ...
    def pileup(
        self,
        contig: Optional[str] = ...,
        start: Optional[int] = ...,
        stop: Optional[int] = ...,
        region: Optional[str] = ...,
        reference: Optional[str] = ...,
        end: Optional[int] = ...,
        truncate: bool = ...,
        max_depth: int = ...,
        stepper: str = ...,
        fastafile: Optional[FastaFile] = ...,
        ignore_overlaps: bool = ...,
        flag_filter: int = ...,
        flag_require: int = ...,
        ignore_orphans: bool = ...,
        min_base_quality: int = ...,
        adjust_capq_threshold: int = ...,
        min_mapping_quality: int = ...,
        compute_baq: bool = ...,
        redo_baq: bool = ...,
    ) -> IteratorColumn: ...
    def count(
        self,
        contig: Optional[str] = ...,
        start: Optional[int] = ...,
        stop: Optional[int] = ...,
        region: Optional[str] = ...,
        until_eof: bool = ...,
        read_callback: Union[str, Callable[[AlignedSegment], bool]] = ...,
        reference: Optional[str] = ...,
        end: Optional[int] = ...,
    ) -> int: ...
    def count_coverage(
        self,
        contig: Optional[str] = ...,
        start: Optional[int] = ...,
        stop: Optional[int] = ...,
        region: Optional[str] = ...,
        quality_threshold: int = ...,
        read_callback: Union[str, Callable[[AlignedSegment], bool]] = ...,
        reference: Optional[str] = ...,
        end: Optional[int] = ...,
    ) -> Tuple[array.array, array.array, array.array, array.array]: ...
    def find_introns_slow(
        self, read_iterator: Iterable[AlignedSegment]
    ) -> Dict[Tuple[int, int], int]: ...
    def find_introns(
        self, read_iterator: Iterable[AlignedSegment]
    ) -> Dict[Tuple[int, int], int]: ...
    def count_junction(
        self,
        read_iterator: Iterable[AlignedSegment],
        donor_site: int,
        acceptor_site: int,
        forward_strand: bool,
        strandedness: Optional[str],
        sam_options: dict,
        etype: str,
        no_match_splice_partner: bool
    ) -> Dict[str, set]: ...
    def close(self) -> None: ...
    def write(self, read: AlignedSegment) -> int: ...
    def __enter__(self) -> AlignmentFile: ...
    def __exit__(self, exc_type, exc_value, traceback): ...
    @property
    def mapped(self) -> int: ...
    @property
    def unmapped(self) -> int: ...
    @property
    def nocoordinate(self) -> int: ...
    def get_index_statistics(self) -> List[IndexStats]: ...
    def __iter__(self) -> AlignmentFileIterator: ...
    def __next__(self) -> AlignedSegment: ...
    def is_valid_tid(self, tid: int) -> bool: ...
    def get_tid(self, reference: str) -> int: ...
    def get_reference_name(self, tid: int) -> str: ...
    def get_reference_length(self, reference: str) -> int: ...
    @property
    def nreferences(self) -> int: ...
    @property
    def references(self) -> Tuple[str, ...]: ...
    @property
    def lengths(self) -> Tuple[int, ...]: ...
    @property
    def reference_filename(self) -> Optional[str]: ...
    @property
    def header(self) -> AlignmentHeader: ...

class IteratorRow:
    def __iter__(self) -> IteratorRow: ...
    def __next__(self) -> AlignedSegment: ...

class IteratorRowAll(IteratorRow): ...
class IteratorRowAllRefs(IteratorRow): ...
class IteratorRowHead(IteratorRow): ...
class IteratorRowRegion(IteratorRow): ...
class IteratorRowSelection(IteratorRow): ...

class IteratorColumn:
    def __iter__(self) -> IteratorColumn: ...
    def __next__(self) -> PileupColumn: ...
    @property
    def seq_len(self) -> int: ...
    def add_reference(self, fastafile: FastaFile) -> None: ...
    def has_reference(self) -> bool: ...

class IteratorColumnAll(IteratorColumn): ...
class IteratorColumnAllRefs(IteratorColumn): ...
class IteratorColumnRegion(IteratorColumn): ...

class SNPCall:
    @property
    def tid(self) -> int: ...
    @property
    def pos(self) -> int: ...
    @property
    def reference_base(self) -> str: ...
    @property
    def genotype(self) -> str: ...
    @property
    def consensus_quality(self) -> int: ...
    @property
    def snp_quality(self) -> int: ...
    @property
    def mapping_quality(self) -> int: ...
    @property
    def coverage(self) -> int: ...

class IndexedReads:
    def __init__(
        self, samfile: AlignmentFile, multiple_iterators: bool = ...
    ) -> None: ...
    def build(self) -> None: ...
    def find(self, query_name: str) -> IteratorRow: ...
