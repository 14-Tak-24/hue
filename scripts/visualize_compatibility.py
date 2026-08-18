#!/usr/bin/env python3
"""
Soul Compatibility Visualization
Generate visual representations of soul compatibility and relationships
"""

import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Set, Tuple
from collections import defaultdict

# Add the src directory to the path for package imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from modules.souls_manager import SoulsManager


class CompatibilityVisualizer:
    """Generate visual representations of soul compatibility"""
    
    def __init__(self, data_path: str = None):
        """Initialize the visualizer"""
        if data_path is None:
            data_path = Path(__file__).parent / "src" / "data" / "souls_entities.json"
        
        self.souls_manager = SoulsManager(str(data_path))
        self.souls = self.souls_manager.get_all_souls()
        
    def generate_compatibility_matrix(self, threshold: float = 50.0) -> str:
        """Generate a text-based compatibility matrix"""
        soul_ids = [soul.id for soul in self.souls]
        soul_names = {soul.id: soul.name for soul in self.souls}
        
        # Calculate compatibility matrix
        matrix = {}
        for i, soul1_id in enumerate(soul_ids):
            for j, soul2_id in enumerate(soul_ids):
                if i <= j:  # Only calculate upper triangle
                    score = self.souls_manager.get_soul_compatibility_score(soul1_id, soul2_id)
                    matrix[(soul1_id, soul2_id)] = score
        
        # Generate ASCII matrix
        output = []
        output.append("SOUL COMPATIBILITY MATRIX")
        output.append("=" * 80)
        output.append(f"Threshold: {threshold}%")
        output.append("")
        
        # Header row
        header = "          " + "".join(f"{soul_names[sid][:8]:<10}" for sid in soul_ids[:10])
        output.append(header)
        output.append("-" * len(header))
        
        # Matrix rows
        for i, soul1_id in enumerate(soul_ids[:10]):
            row_name = soul_names[soul1_id][:8]
            row = f"{row_name:<10}"
            
            for j, soul2_id in enumerate(soul_ids[:10]):
                if i > j:
                    score = matrix[(soul2_id, soul1_id)]
                else:
                    score = matrix[(soul1_id, soul2_id)]
                
                # Display score as character
                if score >= 80:
                    char = "█"
                elif score >= 60:
                    char = "▓"
                elif score >= 40:
                    char = "▒"
                elif score >= threshold:
                    char = "░"
                else:
                    char = "."
                
                row += f"{char:<10}"
            
            output.append(row)
        
        output.append("")
        output.append("Legend: █ = 80%+, ▓ = 60-79%, ▒ = 40-59%, ░ = threshold+, . = below threshold")
        
        return "\n".join(output)
    
    def generate_network_graph(self, threshold: float = 50.0) -> str:
        """Generate a text-based network graph"""
        output = []
        output.append("SOUL NETWORK GRAPH")
        output.append("=" * 80)
        output.append(f"Threshold: {threshold}%")
        output.append("")
        
        # Generate network map
        network_map = self.souls_manager.get_soul_network_map()
        soul_names = {soul.id: soul.name for soul in self.souls}
        
        # Count connections
        connection_counts = defaultdict(int)
        for soul_id, connections in network_map.items():
            connection_counts[soul_id] = len(connections)
        
        # Sort by connection count
        sorted_souls = sorted(connection_counts.items(), key=lambda x: x[1], reverse=True)
        
        output.append("Most Connected Souls:")
        output.append("-" * 40)
        for soul_id, count in sorted_souls[:10]:
            output.append(f"  {soul_names[soul_id]:<20} {count} connections")
        
        output.append("")
        output.append("Network Clusters (Shared Platforms):")
        output.append("-" * 40)
        
        # Find platform-based clusters
        platform_clusters = defaultdict(list)
        for soul in self.souls:
            for platform in soul.platforms:
                platform_clusters[platform].append(soul.id)
        
        # Show platforms with most souls
        sorted_platforms = sorted(platform_clusters.items(), key=lambda x: len(x[1]), reverse=True)
        for platform, soul_ids in sorted_platforms[:5]:
            output.append(f"\n{platform} ({len(soul_ids)} souls):")
            for soul_id in soul_ids:
                output.append(f"  • {soul_names[soul_id]}")
        
        return "\n".join(output)
    
    def generate_compatibility_report(self, soul_id: str, threshold: float = 50.0) -> str:
        """Generate detailed compatibility report for a specific soul"""
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            soul = self.souls_manager.get_soul_by_name(soul_id)
        
        if not soul:
            return f"Soul not found: {soul_id}"
        
        compatible = self.souls_manager.find_compatible_souls(soul.id, threshold)
        
        output = []
        output.append(f"COMPATIBILITY REPORT: {soul.name}")
        output.append("=" * 80)
        output.append(f"Archetype: {soul.archetype}")
        output.append(f"Rarity: {soul.rarity}")
        output.append(f"Tier: {soul.tier}")
        output.append(f"Platforms: {', '.join(soul.platforms)}")
        output.append("")
        output.append(f"Compatible Souls (threshold: {threshold}%):")
        output.append("-" * 40)
        
        if not compatible:
            output.append("No compatible souls found above threshold")
        else:
            for compatible_soul, score in compatible:
                output.append(f"\n{compatible_soul.name} ({compatible_soul.archetype}) - {score:.1f}%")
                output.append(f"  Shared Platforms: {', '.join(set(soul.platforms) & set(compatible_soul.platforms))}")
                output.append(f"  Tier Match: {'Yes' if soul.tier == compatible_soul.tier else 'No'}")
                output.append(f"  Rarity Difference: {abs(['Common', 'Rare', 'Legendary'].index(soul.rarity) - ['Common', 'Rare', 'Legendary'].index(compatible_soul.rarity))}")
        
        return "\n".join(output)
    
    def generate_platform_matrix(self) -> str:
        """Generate a platform presence matrix"""
        output = []
        output.append("PLATFORM PRESENCE MATRIX")
        output.append("=" * 80)
        output.append("")
        
        # Get all platforms
        all_platforms = set()
        for soul in self.souls:
            all_platforms.update(soul.platforms)
        
        sorted_platforms = sorted(all_platforms)
        
        # Header row
        header = "Soul Name        " + "".join(f"{platform[:3]:<4}" for platform in sorted_platforms[:15])
        output.append(header)
        output.append("-" * len(header))
        
        # Matrix rows
        for soul in self.souls[:15]:  # Show first 15 souls
            row_name = soul.name[:15]
            row = f"{row_name:<17}"
            
            for platform in sorted_platforms[:15]:
                if platform in soul.platforms:
                    row += " X  "
                else:
                    row += " .  "
            
            output.append(row)
        
        output.append("")
        output.append(f"Total Platforms: {len(all_platforms)}")
        output.append(f"Showing first 15 souls and platforms")
        
        return "\n".join(output)
    
    def export_compatibility_data(self, output_file: str, threshold: float = 50.0):
        """Export compatibility data to JSON file"""
        soul_ids = [soul.id for soul in self.souls]
        soul_names = {soul.id: soul.name for soul in self.souls}
        
        compatibility_data = {
            'threshold': threshold,
            'generated_at': str(Path.cwd()),
            'souls': [
                {
                    'id': soul.id,
                    'name': soul.name,
                    'archetype': soul.archetype,
                    'rarity': soul.rarity,
                    'tier': soul.tier,
                    'platforms': soul.platforms
                }
                for soul in self.souls
            ],
            'compatibility_matrix': {},
            'compatible_pairs': []
        }
        
        # Calculate all compatibility scores
        for i, soul1_id in enumerate(soul_ids):
            for j, soul2_id in enumerate(soul_ids):
                if i < j:  # Only calculate each pair once
                    score = self.souls_manager.get_soul_compatibility_score(soul1_id, soul2_id)
                    compatibility_data['compatibility_matrix'][f"{soul1_id}_{soul2_id}"] = score
                    
                    if score >= threshold:
                        compatibility_data['compatible_pairs'].append({
                            'soul1': soul1_id,
                            'soul2': soul2_id,
                            'score': score
                        })
        
        # Write to file
        with open(output_file, 'w') as f:
            json.dump(compatibility_data, f, indent=2)
        
        return f"Compatibility data exported to {output_file}"


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Generate soul compatibility visualizations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate compatibility matrix
  python visualize_compatibility.py matrix --threshold 60
  
  # Generate network graph
  python visualize_compatibility.py network
  
  # Generate compatibility report for specific soul
  python visualize_compatibility.py report soul_001
  
  # Generate platform matrix
  python visualize_compatibility.py platform
  
  # Export compatibility data to JSON
  python visualize_compatibility.py export compatibility_data.json
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Visualization type')
    
    # Matrix command
    matrix_parser = subparsers.add_parser('matrix', help='Generate compatibility matrix')
    matrix_parser.add_argument('--threshold', type=float, default=50.0, help='Compatibility threshold')
    
    # Network command
    network_parser = subparsers.add_parser('network', help='Generate network graph')
    network_parser.add_argument('--threshold', type=float, default=50.0, help='Compatibility threshold')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate compatibility report for specific soul')
    report_parser.add_argument('soul_id', help='Soul ID or name')
    report_parser.add_argument('--threshold', type=float, default=50.0, help='Compatibility threshold')
    
    # Platform command
    subparsers.add_parser('platform', help='Generate platform presence matrix')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export compatibility data to JSON')
    export_parser.add_argument('output_file', help='Output JSON file path')
    export_parser.add_argument('--threshold', type=float, default=50.0, help='Compatibility threshold')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    visualizer = CompatibilityVisualizer()
    
    try:
        if args.command == 'matrix':
            output = visualizer.generate_compatibility_matrix(args.threshold)
            print(output)
            
        elif args.command == 'network':
            output = visualizer.generate_network_graph(args.threshold)
            print(output)
            
        elif args.command == 'report':
            output = visualizer.generate_compatibility_report(args.soul_id, args.threshold)
            print(output)
            
        elif args.command == 'platform':
            output = visualizer.generate_platform_matrix()
            print(output)
            
        elif args.command == 'export':
            result = visualizer.export_compatibility_data(args.output_file, args.threshold)
            print(result)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())