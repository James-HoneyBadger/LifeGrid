"""
RLE (Run Length Encoded) format support for patterns.

RLE is a standard format for representing cellular automaton patterns
compactly. This module provides parsing and encoding capabilities.
"""

import re
from typing import Tuple, List, Optional, Dict
import numpy as np


class RLEParser:
    """Parse RLE format patterns.
    
    RLE format specification:
    - Lines starting with '#' are comments
    - Header line: x = width, y = height, rule = B3/S23
    - Pattern lines use run-length encoding:
      - 'b' = dead cell
      - 'o' = alive cell  
      - '$' = end of line
      - '!' = end of pattern
      - digits before a character indicate repetition
    """
    
    @staticmethod
    def parse(rle_string: str) -> Tuple[np.ndarray, Dict[str, str]]:
        """Parse an RLE string into a grid.
        
        Args:
            rle_string: RLE format string
            
        Returns:
            Tuple of (grid, metadata_dict)
            
        Raises:
            ValueError: If RLE format is invalid
        """
        lines = rle_string.strip().split('\n')
        
        # Extract comments and metadata
        comments = []
        metadata = {}
        pattern_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('#'):
                comments.append(line[1:].strip())
            elif line.startswith('x'):
                # Parse header
                metadata.update(RLEParser._parse_header(line))
            else:
                pattern_lines.append(line)
        
        # Join pattern lines
        pattern_data = ''.join(pattern_lines)
        
        # Get dimensions from header or infer them
        width = int(metadata.get('x', 0))
        height = int(metadata.get('y', 0))
        
        # Parse pattern
        grid = RLEParser._decode_pattern(pattern_data, width, height)
        
        # Add comments to metadata
        if comments:
            metadata['comments'] = comments
        
        return grid, metadata
    
    @staticmethod
    def _parse_header(header: str) -> Dict[str, str]:
        """Parse RLE header line.
        
        Args:
            header: Header line string
            
        Returns:
            Dictionary of header fields
        """
        metadata = {}
        
        # Extract x, y, rule using regex
        x_match = re.search(r'x\s*=\s*(\d+)', header, re.IGNORECASE)
        y_match = re.search(r'y\s*=\s*(\d+)', header, re.IGNORECASE)
        rule_match = re.search(r'rule\s*=\s*([^\s,]+)', header, re.IGNORECASE)
        
        if x_match:
            metadata['x'] = x_match.group(1)
        if y_match:
            metadata['y'] = y_match.group(1)
        if rule_match:
            metadata['rule'] = rule_match.group(1)
        
        return metadata
    
    @staticmethod
    def _decode_pattern(
        pattern: str,
        width: int,
        height: int
    ) -> np.ndarray:
        """Decode RLE pattern string into grid.
        
        Args:
            pattern: RLE pattern string
            width: Pattern width (0 to auto-detect)
            height: Pattern height (0 to auto-detect)
            
        Returns:
            Grid array
        """
        # Remove whitespace and end marker
        pattern = pattern.replace(' ', '').replace('\t', '')
        if pattern.endswith('!'):
            pattern = pattern[:-1]
        
        # Parse pattern
        rows = []
        current_row = []
        i = 0
        
        while i < len(pattern):
            # Read run count
            run_count = ''
            while i < len(pattern) and pattern[i].isdigit():
                run_count += pattern[i]
                i += 1
            
            if i >= len(pattern):
                break
            
            count = int(run_count) if run_count else 1
            char = pattern[i]
            
            if char == 'b':
                # Dead cells
                current_row.extend([0] * count)
            elif char == 'o':
                # Alive cells
                current_row.extend([1] * count)
            elif char == '$':
                # End of line
                rows.extend([current_row] * count)
                current_row = []
            else:
                # Unknown character, skip
                pass
            
            i += 1
        
        # Add last row if not empty
        if current_row:
            rows.append(current_row)
        
        # Determine dimensions
        if not rows:
            return np.zeros((height or 1, width or 1), dtype=np.uint8)
        
        actual_width = max(len(row) for row in rows) if rows else 0
        actual_height = len(rows)
        
        # Use provided dimensions or actual dimensions
        final_width = width if width > 0 else actual_width
        final_height = height if height > 0 else actual_height
        
        # Create grid
        grid = np.zeros((final_height, final_width), dtype=np.uint8)
        
        # Fill grid with pattern
        for y, row in enumerate(rows):
            if y >= final_height:
                break
            for x, cell in enumerate(row):
                if x >= final_width:
                    break
                grid[y, x] = cell
        
        return grid
    
    @staticmethod
    def parse_file(filepath: str) -> Tuple[np.ndarray, Dict[str, str]]:
        """Parse RLE file.
        
        Args:
            filepath: Path to RLE file
            
        Returns:
            Tuple of (grid, metadata_dict)
        """
        with open(filepath, 'r') as f:
            rle_string = f.read()
        
        return RLEParser.parse(rle_string)


class RLEEncoder:
    """Encode grids to RLE format.
    
    This class converts grid patterns to RLE format for compact
    storage and sharing.
    """
    
    @staticmethod
    def encode(
        grid: np.ndarray,
        rule: str = "B3/S23",
        comments: Optional[List[str]] = None,
        line_width: int = 70
    ) -> str:
        """Encode a grid to RLE format.
        
        Args:
            grid: Grid to encode
            rule: Rule string (e.g., "B3/S23")
            comments: Optional list of comment lines
            line_width: Maximum line width
            
        Returns:
            RLE format string
        """
        height, width = grid.shape
        
        # Build RLE string
        lines = []
        
        # Add comments
        if comments:
            for comment in comments:
                lines.append(f"# {comment}")
        
        # Add header
        lines.append(f"x = {width}, y = {height}, rule = {rule}")
        
        # Encode pattern
        pattern = RLEEncoder._encode_pattern(grid, line_width)
        lines.extend(pattern)
        
        return '\n'.join(lines)
    
    @staticmethod
    def _encode_pattern(grid: np.ndarray, line_width: int) -> List[str]:
        """Encode grid pattern to RLE.
        
        Args:
            grid: Grid to encode
            line_width: Maximum line width
            
        Returns:
            List of pattern lines
        """
        height, width = grid.shape
        pattern_parts = []
        
        for y in range(height):
            row = grid[y]
            
            # Encode row with run-length encoding
            x = 0
            while x < width:
                # Count consecutive cells of same value
                value = row[x]
                count = 1
                while x + count < width and row[x + count] == value:
                    count += 1
                
                # Encode run
                char = 'o' if value != 0 else 'b'
                if count == 1:
                    pattern_parts.append(char)
                else:
                    pattern_parts.append(f"{count}{char}")
                
                x += count
            
            # Add end-of-line marker (skip for last row)
            if y < height - 1:
                pattern_parts.append('$')
        
        # Add end-of-pattern marker
        pattern_parts.append('!')
        
        # Join into lines with max width
        lines = []
        current_line = ''
        
        for part in pattern_parts:
            if len(current_line) + len(part) > line_width and current_line:
                lines.append(current_line)
                current_line = part
            else:
                current_line += part
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    @staticmethod
    def encode_to_file(
        grid: np.ndarray,
        filepath: str,
        rule: str = "B3/S23",
        comments: Optional[List[str]] = None
    ) -> None:
        """Encode grid to RLE file.
        
        Args:
            grid: Grid to encode
            filepath: Output file path
            rule: Rule string
            comments: Optional comments
        """
        rle_string = RLEEncoder.encode(grid, rule, comments)
        
        with open(filepath, 'w') as f:
            f.write(rle_string)
